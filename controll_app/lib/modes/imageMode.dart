import 'dart:io';

import 'package:image_picker/image_picker.dart';
import 'package:image_cropper/image_cropper.dart';
import 'package:image/image.dart' as imagelib;
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../connection.dart';
import '../connectionPage.dart';
import '../widgets/page.dart';

class ImageModePage extends StatefulWidget {
  final Connection connection;

  ImageModePage({
    Key key,
    @required this.connection
  }): super(key: key);

  @override
  _ImageModePageState createState() => _ImageModePageState();
}

class _ImageModePageState extends State < ImageModePage > implements ConnectionInterface {
  String _image;
  final picker = ImagePicker();
  double width = 20;
  double height = 15;

  @override
  Widget build(BuildContext context) {
    return DefaultPage("Image", GestureDetector(
      behavior: HitTestBehavior.translucent,
      onTap: () {
        FocusScope.of(context).requestFocus(new FocusNode());
      },
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: < Widget > [
          Center(
            child: _buildImagePicker()
          ),

          SizedBox(height: 10),
          Visibility(
            //visible: _image != null,
            visible: true,
            child: SizedBox(width: double.infinity,
              child: RaisedButton(
                onPressed: sendImage,
                child: Text('Set Image'),
              )), )
        ]
      ),
    ), widget.connection);
  }

  void sendImage() {
    Map < String, dynamic > settings = Map < String, dynamic > ();
    
    imagelib.Image img = imagelib.decodeImage(base64.decode(_image.split(',').last));
    img = imagelib.copyResize(img, height: height.floor(), width: width.floor());
    settings['image'] = base64Encode(imagelib.encodeJpg(img));
    
    /*String imageString = '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';
    settings['image'] = imageString;*/
    widget.connection.sendModeSettings(settings);
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
    widget.connection.setParent(this);
    super.initState();
  }
  @override
  void dispose() {
    super.dispose();
  }

    Widget _buildImagePicker() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [GestureDetector(
        onTap: () {
          _showPicker(context);
        },
        child: Container(
          child: _image != null ?
          ClipRRect(
            child: Image.memory(base64.decode(_image.split(',').last),
              width: width*15,
              height: height*15,
              fit: BoxFit.cover,
            ),

          ) :
          Container(
            decoration: BoxDecoration(
              color: Theme.of(context).accentColor,
              borderRadius: BorderRadius.circular(50)),
            width: 50,
            height: 50,
            child: Icon(
              Icons.camera_alt,
              color: Theme.of(context).primaryColor
            ),
          ),
        ),
      )],
    );
  }

  void _showPicker(context) {
    showModalBottomSheet(
      context: context,
      builder: (BuildContext bc) {
        return SafeArea(
          child: Container(
            child: new Wrap(
              children: < Widget > [
                new ListTile(
                  leading: new Icon(Icons.photo_library),
                  title: new Text('Photo Library'),
                  onTap: () {
                    _imgFromGallery();
                    Navigator.of(context).pop();
                  }),
                new ListTile(
                  leading: new Icon(Icons.photo_camera),
                  title: new Text('Camera'),
                  onTap: () {
                    _imgFromCamera();
                    Navigator.of(context).pop();
                  },
                ),
              ],
            ),
          ),
        );
      }
    );
  }

  _imgFromCamera() async {
    ImagePicker imagePicker = new ImagePicker();
    PickedFile image = await imagePicker.getImage(
      source: ImageSource.camera, imageQuality: 100
    );
    File imageFile = await _cropImage(image.path);

    setState(() {
      _image = base64Encode(imageFile.readAsBytesSync());
    });
  }

  _imgFromGallery() async {
    ImagePicker imagePicker = new ImagePicker();
    PickedFile image = await imagePicker.getImage(
      source: ImageSource.gallery, imageQuality: 100
    );
    File imageFile = await _cropImage(image.path);

    setState(() {
      _image = base64Encode(imageFile.readAsBytesSync());
    });
  }
    /// Crop Image
  Future < File > _cropImage(filePath) async {
    return await ImageCropper.cropImage(
      aspectRatio: CropAspectRatio(ratioX: width, ratioY: height),
      sourcePath: filePath,
    );
  }

}