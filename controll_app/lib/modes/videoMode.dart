/*import 'dart:async';
import 'dart:ffi';
import 'dart:io';
import 'dart:typed_data';

import 'package:image/image.dart' as imagelib;
import 'package:camera/camera.dart';
import 'dart:ffi' as dartffi;
import 'package:ffi/ffi.dart' as ffi;
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../connection.dart';
import '../connectionPage.dart';
import '../settings.dart';
import '../widgets/page.dart';
import 'package:flutter/services.dart';

final DynamicLibrary stdlib = Platform.isWindows
    ? DynamicLibrary.open('kernel32.dll')
    : DynamicLibrary.process();
typedef PosixMallocNative = Pointer Function(IntPtr);
typedef PosixMalloc = Pointer Function(int);
final PosixMalloc posixMalloc =
    stdlib.lookupFunction<PosixMallocNative, PosixMalloc>('malloc');
    typedef PosixFreeNative = Void Function(Pointer);
typedef PosixFree = void Function(Pointer);
final PosixFree posixFree =
    stdlib.lookupFunction<PosixFreeNative, PosixFree>('free');

typedef PosixCallocNative = Pointer Function(IntPtr num, IntPtr size);
typedef PosixCalloc = Pointer Function(int num, int size);
final PosixCalloc posixCalloc =
    stdlib.lookupFunction<PosixCallocNative, PosixCalloc>('calloc');
typedef convert_func = Pointer < Uint32 > Function(Pointer < Uint8 > , Pointer < Uint8 > , Pointer < Uint8 > , Int32, Int32, Int32, Int32);
typedef Convert = Pointer < Uint32 > Function(Pointer < Uint8 > , Pointer < Uint8 > , Pointer < Uint8 > , int, int, int, int);
typedef WinHeapAllocNative = Pointer Function(Pointer, Uint32, IntPtr);
typedef WinHeapAlloc = Pointer Function(Pointer, int, int);
final WinHeapAlloc winHeapAlloc = stdlib.lookupFunction<WinHeapAllocNative, WinHeapAlloc>('HeapAlloc');
typedef WinHeapFreeNative = Int32 Function(
    Pointer heap, Uint32 flags, Pointer memory);
typedef WinHeapFree = int Function(Pointer heap, int flags, Pointer memory);
final WinHeapFree winHeapFree =
    stdlib.lookupFunction<WinHeapFreeNative, WinHeapFree>('HeapFree');

typedef WinGetProcessHeapFn = Pointer Function();
final WinGetProcessHeapFn winGetProcessHeap = stdlib
    .lookupFunction<WinGetProcessHeapFn, WinGetProcessHeapFn>('GetProcessHeap');
final Pointer processHeap = winGetProcessHeap();

class VideoModePage extends StatefulWidget {
  final Connection connection;

  VideoModePage({
    Key key,
    @required this.connection
  }): super(key: key);

  @override
  _VideoModePageState createState() => _VideoModePageState();
}

class _VideoModePageState extends State < VideoModePage > implements ConnectionInterface {
  double width = 20;
  double height = 15;

  Allocator allocator;

  CameraController _camera;
  bool enableSend = false;
  bool _cameraInitialized = false;
  CameraImage _savedImage;
  imagelib.Image img;
  Timer timer;

  Socket _socket;

  final DynamicLibrary convertImageLib = Platform.isAndroid ?
    DynamicLibrary.open("libconvertImage.so") :
    DynamicLibrary.process();
  Convert conv;

  Widget build(BuildContext context) {
    List < Widget > actions = [];
    actions.add(IconButton(icon: Icon(Icons.settings), onPressed: () {
      Navigator.push(context, MaterialPageRoute(builder: (BuildContext context) => SettingsPage(connection: widget.connection)));
    }));
    return Scaffold(
      appBar: AppBar(
        title: Text("Video"),
        actions: actions
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
          child: Center(
            child:
            (_cameraInitialized) ?
            AspectRatio(aspectRatio: _camera.value.aspectRatio,
              child: CameraPreview(_camera), ) :
            CircularProgressIndicator()
          ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          setState(() {
            enableSend = !enableSend;
          });
        },
        child: Icon(enableSend ? Icons.camera_alt : Icons.camera_alt_outlined, color: enableSend ? Colors.green : Colors.red, ),
      ), // This trailing comma makes auto-formatting nicer for build methods.
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
    );
  }

  void sendImage() {
    if (!enableSend) {
      return;
    }
    if (!isConnected()) {
      print('not connected!');
      return;
    }

    // Allocate memory for the 3 planes of the image
    Pointer < Uint8 > p = allocator.allocate(_savedImage.planes[0].bytes.length);
    Pointer < Uint8 > p1 = allocator.allocate(_savedImage.planes[1].bytes.length);
    Pointer < Uint8 > p2 = allocator.allocate(_savedImage.planes[2].bytes.length);

    // Assign the planes data to the pointers of the image
    Uint8List pointerList = p.asTypedList(_savedImage.planes[0].bytes.length);
    Uint8List pointerList1 = p1.asTypedList(_savedImage.planes[1].bytes.length);
    Uint8List pointerList2 = p2.asTypedList(_savedImage.planes[2].bytes.length);
    pointerList.setRange(0, _savedImage.planes[0].bytes.length, _savedImage.planes[0].bytes);
    pointerList1.setRange(0, _savedImage.planes[1].bytes.length, _savedImage.planes[1].bytes);
    pointerList2.setRange(0, _savedImage.planes[2].bytes.length, _savedImage.planes[2].bytes);

    // Call the convertImage function and convert the YUV to RGB
    Pointer < Uint32 > imgP = conv(p, p1, p2, _savedImage.planes[1].bytesPerRow,
      _savedImage.planes[1].bytesPerPixel, _savedImage.width, _savedImage.height);
    // Get the pointer of the data returned from the function to a List
    List imgData = imgP.asTypedList((_savedImage.width * _savedImage.height));

    // Generate image from the converted data  
    img = imagelib.Image.fromBytes(_savedImage.height, _savedImage.width, imgData);

    // Free the memory space allocated
    // from the planes and the converted data
    allocator.free(p);
    allocator.free(p1);
    allocator.free(p2);
    allocator.free(imgP);

    img = imagelib.copyRotate(img, 90);
    img = imagelib.copyResize(img, height: height.floor(), width: width.floor());

    List < int > msg = imagelib.encodeJpg(img, quality: 70);
    _socket.add(msg);
  }

  void _initializeCamera() async {
    // Get list of cameras of the device
    List < CameraDescription > cameras = await availableCameras();
    // Create the CameraController
    _camera = new CameraController(
      cameras[0], ResolutionPreset.low
    );
    // Initialize the CameraController
    _camera.initialize().then((_) async {
      // Start ImageStream
      await _camera.startImageStream((CameraImage image) =>
        _processCameraImage(image));
      setState(() {
        _cameraInitialized = true;
      });
    });
  }

  void _processCameraImage(CameraImage image) async {
    if (!this.mounted) {
      _camera.stopImageStream();
      _camera.dispose();
      return;
    }
    setState(() {
      _savedImage = image;
    });
  }


  Future < bool > connect() async {
    String address = widget.connection.address;
    int port = 8943;
    print('connecting VIDEO');
    try {
      await close();

      _socket = await Socket.connect(address, port.toInt(), timeout: Duration(seconds: 1));
      /*_socket.handleError((Object e){
        print("An error occured. Redirecting to Connect-Screen.");
        parent.connectionError();
      }, test: (e)=>true);
      _socket.listen((List<int> event) {
        receiveMessage(utf8.decode(event));
      });*/
    } catch (e) {
      print('Could not connect to VIDEO Websocket.');
      return false;
    }

    return true;
  }

  Future < bool > close() async {
    if (!isConnected()) {
      return false;
    }
    print("closing VIDEO...");
    await _socket.flush();
    _socket.close();
    _socket = null;
    return true;
  }

  bool isConnected() {
    if (_socket != null) {
      bool done = false;
      _socket.done.whenComplete(() => done = true);
      return !done;
    }
    return false;
  }



  void receiveMode(Map < String, dynamic > message) {
    Navigator.of(context).pop(message['data']);
  }

  void receiveWelcome(Map < String, dynamic > message) {
    print(message['type']);
  }

  void receiveModes(Map < String, dynamic > message) {
    print(message['type']);
  }

  void connectionError() {
    Navigator.of(context).popUntil((route) => route.isFirst);
    Navigator.pushReplacement(context, MaterialPageRoute(builder: (BuildContext context) => ConnectionPage(connection: widget.connection)));
  }

  @override
  void initState() {
    allocator = new _MallocAllocator();
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
    ]);
    widget.connection.setParent(this);
    // Load the convertImage() function from the library
    conv = convertImageLib
      .lookup < NativeFunction < convert_func >> ('convertImage')
      .asFunction < Convert > ();
    _initializeCamera();
    Timer(Duration(seconds: 1), 
      (){
        connect();
        timer = new Timer.periodic(Duration(milliseconds: 50), (Timer t) => sendImage());
      }
    );
    
    super.initState();
  }
  @override
  void dispose() {
    try {
      _camera.stopImageStream().then((value) => _camera.dispose());
    } catch (e) {}
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.landscapeRight,
      DeviceOrientation.landscapeLeft,
      DeviceOrientation.portraitUp,
      DeviceOrientation.portraitDown,
    ]);
    timer.cancel();
    super.dispose();
  }


}



class _MallocAllocator implements Allocator {
  const _MallocAllocator();

  /// Allocates [byteCount] bytes of of unitialized memory on the native heap.
  ///
  /// For POSIX-based systems, this uses `malloc`. On Windows, it uses
  /// `HeapAlloc` against the default public heap.
  ///
  /// Throws an [ArgumentError] if the number of bytes or alignment cannot be
  /// satisfied.
  // TODO: Stop ignoring alignment if it's large, for example for SSE data.
  @override
  Pointer<T> allocate<T extends NativeType>(int byteCount, {int alignment}) {
    Pointer<T> result;
    if (Platform.isWindows) {
      result = winHeapAlloc(processHeap, /*flags=*/ 0, byteCount).cast();
    } else {
      result = posixMalloc(byteCount).cast();
    }
    if (result.address == 0) {
      throw ArgumentError('Could not allocate $byteCount bytes.');
    }
    return result;
  }

  /// Releases memory allocated on the native heap.
  ///
  /// For POSIX-based systems, this uses `free`. On Windows, it uses `HeapFree`
  /// against the default public heap. It may only be used against pointers
  /// allocated in a manner equivalent to [allocate].
  ///
  /// Throws an [ArgumentError] if the memory pointed to by [pointer] cannot be
  /// freed.
  ///
  // TODO(dartbug.com/36855): Once we have a ffi.Bool type we can use it instead
  // of testing the return integer to be non-zero.
  @override
  void free(Pointer pointer) {
    if (Platform.isWindows) {
      if (winHeapFree(processHeap, /*flags=*/ 0, pointer) == 0) {
        throw ArgumentError('Could not free $pointer.');
      }
    } else {
      posixFree(pointer);
    }
  }
}*/