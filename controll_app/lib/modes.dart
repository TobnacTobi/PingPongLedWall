import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'connection.dart';
import 'connectionPage.dart';
import 'widgets/page.dart';
import 'modes/defaultMode.dart';

class ModesPage extends StatefulWidget {
  final Connection connection;
  final List<String> modes;

  ModesPage({Key key, @required this.connection, @required this.modes})
      : super(key: key);

  @override
  _ModesPageState createState() => _ModesPageState();
}

class _ModesPageState extends State<ModesPage> implements ConnectionInterface{
  List<String> received = new List<String>();
  SharedPreferences prefs;
  bool loading = false;

  @override
  Widget build(BuildContext context) {
    return DefaultPage("Modes", ListView(
      children: widget.modes.map((e) => 
        ListTile(leading: getIconByMode(e), title: Text(e.toUpperCase()), onTap: (){sendMode(e);},)
      ).toList(),
    ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }

  void sendMode(String selectedMode){
    EasyLoading.show(status: 'loading...');
    widget.connection.sendMode(selectedMode);
  }

  void receiveMode(Map<String, dynamic> message){
    print(message);
    EasyLoading.dismiss();
    Navigator.of(context).popUntil((route) => route.isFirst);
    switch (message['data']) {
      case "clock":
        Navigator.pushReplacement(context, MaterialPageRoute(builder: (BuildContext context) => DefaultModePage(connection: widget.connection)));
        break;
      case "colors":
        Navigator.pushReplacement(context, MaterialPageRoute(builder: (BuildContext context) => DefaultModePage(connection: widget.connection)));
        break;
      case "menu":
        Navigator.pushReplacement(context, MaterialPageRoute(builder: (BuildContext context) => DefaultModePage(connection: widget.connection)));
        break;
      default:
        Navigator.pushReplacement(context, MaterialPageRoute(builder: (BuildContext context) => DefaultModePage(connection: widget.connection)));
    }
  }


  void receiveWelcome(Map<String, dynamic> message){
    print(message['type']);
    
  }
  void receiveModes(Map<String, dynamic> message){
    print(message['type']);
  }

  void connectionError(){
    Navigator.of(context).popUntil((route) => route.isFirst);
    Navigator.pushReplacement(context, MaterialPageRoute(builder: (BuildContext context) => ConnectionPage(connection: widget.connection)));
  }

  Icon getIconByMode(String mode){
    switch (mode) {
      case "clock":
        return Icon(Icons.query_builder);
      case "colors":
        return Icon(Icons.invert_colors);
      case "menu":
        return Icon(Icons.menu);
      default:
        return Icon(Icons.star);
    }
  }


  @override
  void initState() {
    widget.modes.remove("mode");
    widget.modes.sort();
    widget.connection.setParent(this);
    super.initState();
  }
  @override
  void dispose() {
    super.dispose();
  }
}