import 'package:controll_app/widgets/buttons.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../connection.dart';
import '../connectionPage.dart';
import '../widgets/page.dart';

class MenuModePage extends StatefulWidget {
  final Connection connection;

  MenuModePage({Key key, @required this.connection})
      : super(key: key);

  @override
  _MenuModePageState createState() => _MenuModePageState();
}

class _MenuModePageState extends State<MenuModePage> implements ConnectionInterface{
  List<String> received = new List<String>();
  SharedPreferences prefs;

  @override
  Widget build(BuildContext context) {
    return DefaultPage("Menu", ControllerButtons(connection: widget.connection), widget.connection);
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