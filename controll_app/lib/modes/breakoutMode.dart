import 'package:controll_app/widgets/buttons.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../connection.dart';
import '../connectionPage.dart';
import '../widgets/page.dart';

class BreakoutModePage extends StatefulWidget {
  final Connection connection;

  BreakoutModePage({Key? key, required this.connection})
      : super(key: key);

  @override
  _BreakoutModePageState createState() => _BreakoutModePageState();
}

class _BreakoutModePageState extends State<BreakoutModePage> implements ConnectionInterface{
  List<String> received = List<String>.empty(growable: true);
  double slidervalue = 50;
  int platformposition = 50;
  SharedPreferences? prefs;

  @override
  Widget build(BuildContext context) {
    return DefaultPage("Slider-Control", 
      Column(
        children: [
          ControllerButtons(connection: widget.connection),
          Slider(value: slidervalue, 
            max: 100,
            min: 0,
            onChanged: (v){
            setState(() {
              slidervalue = v;
            });
            if(slidervalue.floor() != platformposition){
              platformposition = slidervalue.floor();
              sendSlider();
            }
          }),
        ],
      ),
      widget.connection);
  }

  void sendSlider() {
    Map < String, dynamic > settings = Map < String, dynamic > ();
    settings['position'] = platformposition;
    widget.connection.sendModeSettings(settings);
  }

  void receiveMode(Map<String, dynamic> message){
    Navigator.of(context).pop(message['data']);
  }

  void receiveWelcome(Map<String, dynamic> message){
    return;
  }

  void receiveModes(Map<String, dynamic> message){
    return;
  }

  void connectionError(){
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