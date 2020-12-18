import 'dart:convert';
import 'dart:io';

//import 'dart:typed_data';

const int header = 64;

class Connection {
  //WebSocket ws;
  Socket _socket;
  ConnectionInterface parent;
  String defaultAddress = "192.168.178.82";
  num defaultPort = 8942;
  String separator = "|"; // separates messages from each other
  Map<String, dynamic> message = {"type": "HELLO", "data": "", "comment": ""};
  int connection_number = 0;

  Future<bool> connect(String address, num port) async {
    if(address == null || address.length == 0){
      address = defaultAddress;
    }
    if(port == null){
      port = defaultPort;
    }
    print('connecting');
    try {
      await close();

      _socket = await Socket.connect(address, port.toInt(), timeout: Duration(seconds: 2));
      /*_socket.handleError((Object e){
        print("An error occured. Redirecting to Connect-Screen.");
        parent.connectionError();
      }, test: (e)=>true);*/
      _socket.listen((List<int> event) {
        receiveMessage(utf8.decode(event));
      });
    } catch (e) {
      print('Could not connect to Websocket.');
      return false;
    }
    sendHello();

    catchError();

    return true;
  }

  catchError()async{
    try {
      await _socket.done;
      print('WebSocket closed without error');
    } catch (error) {
      print('connection closed with error: ${error}');
      parent.connectionError();
      _socket = null;
    }
  }

  Future<bool> close() async {
    print("closing...");
    if(!isConnected()){
      return false;
    }
    message['type'] = "DISCONNECT";
    sendMessage(message);
    await _socket.flush();
    _socket.close();
    _socket = null;
    return true;
  }

  bool isConnected(){
    if(_socket != null){
      bool done = false;
      _socket.done.whenComplete(() => done = true);
      return !done;
    }
    return false;
  }

  setParent(ConnectionInterface p){
    this.parent = p;
  }

  void sendMessage(Map<String, dynamic> message){
    if(!isConnected()){
      print('not connected!');
      return;
    }
    List<int> msg = utf8.encode(jsonEncode(message) + separator);
    //print(Uint16List.fromList([msg.length]).buffer.asUint8List());
    //var bdata = new ByteData(8);
    //bdata.setInt64(0, msg.length);
    //print(bdata.buffer.asUint8List());
    //_socket.add(bdata.buffer.asUint8List());
    //_socket.flush().then((value) => (){_socket.add(msg);});
    _socket.add(msg);
  }

  void sendHello(){
    message['type'] = "HELLO";
    message['data'] = "";
    sendMessage(message);
  }

  void sendUp(){
    sendDirection("UP");
  }

  void sendDown(){
    sendDirection("DOWN");
  }

  void sendLeft(){
    sendDirection("LEFT");
  }

  void sendRight(){
    sendDirection("RIGHT");
  }

  void sendDirection(String direction){
    message['type'] = "DIRECTION";
    message['data'] = direction;
    sendMessage(message);
  }

  void sendConfirm(){
    message['type'] = "CONFIRM";
    message['data'] = "";
    sendMessage(message);
  }

  void sendReturn(){
    message['type'] = "RETURN";
    message['data'] = "";
    sendMessage(message);
  }

  void sendModes(){
    message['type'] = "MODES";
    message['data'] = "";
    sendMessage(message);
  }

  void sendMode(String selectedMode){
    message['type'] = "MODE";
    message['data'] = selectedMode;
    sendMessage(message);
  }

  void sendModeSettings(Map<String, dynamic> settings){
    message['type'] = "MODESETTINGS";
    message['data'] = json.encode(settings);
    sendMessage(message);
  }

  void sendSettings(Map<String, dynamic> settings){
    message['type'] = "SETTINGS";
    message['data'] = json.encode(settings);
    sendMessage(message);
  }


  receiveMessage(dynamic m){
    Map<String, dynamic> msg = json.decode(m);
    switch (msg['type']) {
      case "WELCOME":
        connection_number = int.parse(msg['data']);
        parent.receiveWelcome(msg);
        break;
      case "MODES":
        connection_number = int.parse(msg['comment']);
        parent.receiveModes(msg);
        break;
      case "MODE":
        parent.receiveMode(msg);
        break;
      default:
        print("Undefined message:");
        print(msg);
    }
  }
}

class ConnectionInterface{
  void receiveWelcome(Map<String, dynamic> message){
    return;
  }
  void receiveModes(Map<String, dynamic> message){
    return;
  }
  void receiveMode(Map<String, dynamic> message){
    print(message['type']);
  }
  void connectionError(){
    print('conn err');
  }
}