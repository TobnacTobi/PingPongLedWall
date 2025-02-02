import 'package:controll_app/widgets/buttons.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../connection.dart';
import '../connectionPage.dart';
import '../widgets/page.dart';

class DefaultModePage extends StatefulWidget {
  final Connection connection;

  DefaultModePage({Key? key, required this.connection})
      : super(key: key);

  @override
  _DefaultModePageState createState() => _DefaultModePageState();
}

class _DefaultModePageState extends State<DefaultModePage> implements ConnectionInterface{
  List<String> received = List<String>.empty(growable: true);
  SharedPreferences? prefs;

  @override
  Widget build(BuildContext context) {
    return DefaultPage("Controller", ControllerButtons(connection: widget.connection), widget.connection);
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