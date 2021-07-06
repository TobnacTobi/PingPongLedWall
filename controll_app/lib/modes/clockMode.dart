import 'dart:convert';

import 'package:controll_app/widgets/buttons.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';

import '../connection.dart';
import '../connectionPage.dart';
import '../widgets/page.dart';

class ClockModePage extends StatefulWidget {
  final Connection connection;

  ClockModePage({
    Key key,
    @required this.connection
  }): super(key: key);

  @override
  _ClockModePageState createState() => _ClockModePageState();
}

class _ClockModePageState extends State < ClockModePage > implements ConnectionInterface {
  List < String > _colorStyles = < String > ['solid', 'fadeHorizontal', 'fadeVertical', 'rainbow'];

  bool _showTextColor = false;
  bool _showBackgroundColor = false;
  String _textStyle = "solid";
  String _backgroundStyle = "solid";
  Color _textColor0 = Colors.white;
  Color _textColor1 = Colors.grey;
  Color _backgroundColor0 = Colors.black;
  Color _backgroundColor1 = Colors.grey;


  @override
  Widget build(BuildContext context) {
    return DefaultPage("Clock", GestureDetector(
      behavior: HitTestBehavior.translucent,
      onTap: () {
        FocusScope.of(context).requestFocus(new FocusNode());
      },
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: < Widget > [
          // Colors

          Row(children: [Checkbox(value: _showTextColor, activeColor: Colors.deepOrange, onChanged: (v) {
              setState(() {
                _showTextColor = v;
              });
            }),
            Text('Clock Color'),
            Visibility(visible: _showTextColor,
              child: Row(children: [
                SizedBox(width: 20),
                Text('Style: '),
                DropdownButton(items: [
                  DropdownMenuItem(child: Text('solid'), value: 'solid'),
                  DropdownMenuItem(child: Text('fadeHorizontal'), value: 'fadeHorizontal'),
                  DropdownMenuItem(child: Text('fadeVertical'), value: 'fadeVertical'),
                  DropdownMenuItem(child: Text('rainbow'), value: 'rainbow'),
                ], value: _textStyle, onChanged: (v) {
                  setState(() {
                    _textStyle = v;
                  });
                })
              ], ))
          ], ),
          Visibility(
            visible: _showTextColor && !_textStyle.startsWith('rainbow'),
            child: Row(children: [
              SizedBox(width: 15),
              RaisedButton(onPressed: (){
                showDialog(context: context, builder: (_) => getAlertDialog(type: 'text', number: 0));
              }, child: Text('ChangeMe', style: TextStyle(color: Colors.black),), color: _textColor0,),
              SizedBox(width: 30),
              Visibility(
                visible: _showTextColor && _textStyle.startsWith('fade'),
                child: RaisedButton(onPressed: (){
                showDialog(context: context, builder: (_) => getAlertDialog(type: 'text', number: 1));
              }, child: Text('ChangeMe', style: TextStyle(color: Colors.black),),color: _textColor1),
              ),
            ], )
          ),

          Row(children: [Checkbox(value: _showBackgroundColor, activeColor: Colors.deepOrange, onChanged: (v) {
              setState(() {
                _showBackgroundColor = v;
              });
            }),
            Text('Background Color'),
            Visibility(visible: _showBackgroundColor,
              child: Row(children: [
                SizedBox(width: 20),
                Text('Style: '),
                DropdownButton(items: [
                  DropdownMenuItem(child: Text('solid'), value: 'solid'),
                  DropdownMenuItem(child: Text('fadeHorizontal'), value: 'fadeHorizontal'),
                  DropdownMenuItem(child: Text('fadeVertical'), value: 'fadeVertical'),
                  DropdownMenuItem(child: Text('rainbow'), value: 'rainbow'),
                ], value: _backgroundStyle, onChanged: (v) {
                  setState(() {
                    _backgroundStyle = v;
                  });
                })
              ], ))
          ], ),
          Visibility(
            visible: _showBackgroundColor && !_backgroundStyle.startsWith('rainbow'),
            child: Row(children: [
              SizedBox(width: 15),
              RaisedButton(onPressed: (){
                showDialog(context: context, builder: (_) => getAlertDialog(type: 'background', number: 0));
              }, child: Text('ChangeMe', style: TextStyle(color: Colors.black),),color: _backgroundColor0),
              SizedBox(width: 30),
              Visibility(
                visible: _showBackgroundColor && _backgroundStyle.startsWith('fade'),
                child: RaisedButton(onPressed: (){
                showDialog(context: context, builder: (_) => getAlertDialog(type: 'background', number: 1));
              }, child: Text('ChangeMe', style: TextStyle(color: Colors.black),),color: _backgroundColor1),
              ),
            ], )
          ),

          SizedBox(height: 10),
          SizedBox(width: double.infinity,
            child: RaisedButton(
              onPressed: sendColors,
              child: Text('Text setzen'),
            )),
          //ControllerButtons(handleClicks),
        ]
      ),
    ), widget.connection);
  }

  void sendColors() {
    Map < String, dynamic > textsettings = Map<String, dynamic>();
    if(!_showTextColor){
      _textStyle = 'solid';
      _textColor0 = Colors.white;
    }
    if(!_showBackgroundColor){
      _backgroundStyle = 'solid';
      _backgroundColor0 = Colors.black;
    }
    textsettings['textcolor'] = getTextColor();
    textsettings['backgroundcolor'] = getBackgroundColor();
    widget.connection.sendModeSettings(textsettings);
  }

  String getTextColor() {
    return json.encode({
      'style': _textStyle,
      'color0': json.encode({'r': _textColor0.red, 'g': _textColor0.green, 'b': _textColor0.blue, 'a': _textColor0.alpha}),
      'color1': json.encode({'r': _textColor1.red, 'g': _textColor1.green, 'b': _textColor1.blue, 'a': _textColor1.alpha})
    });
  }

  String getBackgroundColor() {
    return json.encode({
      'style': _backgroundStyle,
      'color0': json.encode({'r': _backgroundColor0.red, 'g': _backgroundColor0.green, 'b': _backgroundColor0.blue, 'a': _backgroundColor0.alpha}),
      'color1': json.encode({'r': _backgroundColor1.red, 'g': _backgroundColor1.green, 'b': _backgroundColor1.blue, 'a': _backgroundColor1.alpha})
    });
  }

  void receiveMode(Map<String, dynamic> message){
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

  Widget getAlertDialog({
    String type = 'text',
    int number = 0
  }) {
    Color currentColor = null;
    if (type == 'text') {
      if (number == 0) {
        currentColor = _textColor0;
      } else if (number == 1) {
        currentColor = _textColor1;
      }
    } else if (type == 'background') {
      if (number == 0) {
        currentColor = _backgroundColor0;
      } else if (number == 1) {
        currentColor = _backgroundColor1;
      }
    }

    return AlertDialog(
      title: const Text('Pick a color!'),
        content: SingleChildScrollView(
          child: ColorPicker(
            pickerColor: currentColor,
            onColorChanged: (c) {
              setState(() {
                  if (type == 'text') {
                    if (number == 0) {
                      _textColor0 = currentColor;
                    } else if (number == 1) {
                      _textColor1 = currentColor;
                    }
                  } else if (type == 'background') {
                    if (number == 0) {
                      _backgroundColor0 = currentColor;
                    } else if (number == 1) {
                      _backgroundColor1 = currentColor;
                    }
                  }
              });
              sendColors();
              setState(() {
                currentColor = c;
              });
            },
            showLabel: true,displayThumbColor: true,
            pickerAreaHeightPercent: 0.8,
          ),
        ),
        actions: < Widget > [
          FlatButton(
            child: const Text('Set'),
              onPressed: () {
                setState(() {
                  if (type == 'text') {
                    if (number == 0) {
                      _textColor0 = currentColor;
                    } else if (number == 1) {
                      _textColor1 = currentColor;
                    }
                  } else if (type == 'background') {
                    if (number == 0) {
                      _backgroundColor0 = currentColor;
                    } else if (number == 1) {
                      _backgroundColor1 = currentColor;
                    }
                  }
                });
                Navigator.of(context).pop();
              },
          ),
        ],
    );
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