import 'dart:io';

import 'package:image/image.dart' as imagelib;
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../connection.dart';
import '../connectionPage.dart';
import '../widgets/page.dart';

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
  String _image;
  double width = 20;
  double height = 15;

  @override
  Widget build(BuildContext context) {
    return DefaultPage("Video", GestureDetector(
      behavior: HitTestBehavior.translucent,
      onTap: () {
        FocusScope.of(context).requestFocus(new FocusNode());
      },
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: < Widget > [

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


}