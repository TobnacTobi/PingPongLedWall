import 'package:controll_app/modes/textMode.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'connection.dart';
import 'connectionPage.dart';
import 'modes/breakoutMode.dart';
import 'modes/clockMode.dart';
import 'modes/drawMode.dart';
import 'modes/imageMode.dart';
import 'modes/menuMode.dart';
import 'modes/soundMode.dart';
import 'modes/videoMode.dart';
import 'widgets/page.dart';
import 'modes/defaultMode.dart';

class ModesPage extends StatefulWidget {
  final Connection connection;
  List<String> modes;

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
    ), 
    widget.connection,
    );
  }

  void sendMode(String selectedMode){
    EasyLoading.show(status: 'loading...');
    widget.connection.sendMode(selectedMode);
  }

  void receiveMode(Map<String, dynamic> message){
    EasyLoading.dismiss();
    setMode(message['data']);
  }

  void setMode(String mode){
    Navigator.of(context).popUntil((route) => route.isFirst);
    switch (mode) {
      case "clockanalog":
      case "clock":
        Navigator.push(context, MaterialPageRoute(builder: (BuildContext context) => ClockModePage(connection: widget.connection))).then((value){
          returnToThis(value);
        });
        break;
      case "colors":
        Navigator.push(context, MaterialPageRoute(builder: (BuildContext context) => DefaultModePage(connection: widget.connection))).then((value){
          returnToThis(value);
        });
        break;
      case "menu":
        Navigator.push(context, MaterialPageRoute(builder: (BuildContext context) => MenuModePage(connection: widget.connection))).then((value){
          returnToThis(value);
        });
        break;
      case "text":
        Navigator.push(context, MaterialPageRoute(builder: (BuildContext context) => TextModePage(connection: widget.connection))).then((value){
          returnToThis(value);
        });
        break;
      case "draw":
        Navigator.push(context, MaterialPageRoute(builder: (BuildContext context) => DrawModePage(connection: widget.connection))).then((value){
          returnToThis(value);
        });
        break;
      case "image":
        Navigator.push(context, MaterialPageRoute(builder: (BuildContext context) => ImageModePage(connection: widget.connection))).then((value){
          returnToThis(value);
        });
        break;
      case "video":
        Navigator.push(context, MaterialPageRoute(builder: (BuildContext context) => VideoModePage(connection: widget.connection))).then((value){
          returnToThis(value);
        });
        break;
      case 'sound':
        Navigator.push(context, MaterialPageRoute(builder: (BuildContext context) => SoundModePage(connection: widget.connection))).then((value){
          returnToThis(value);
        });
        break;
      case 'breakout':
        Navigator.push(context, MaterialPageRoute(builder: (BuildContext context) => BreakoutModePage(connection: widget.connection))).then((value){
          returnToThis(value);
        });
        break;
      default:
        Navigator.push(context, MaterialPageRoute(builder: (BuildContext context) => DefaultModePage(connection: widget.connection))).then((value){
          returnToThis(value);
        });
    }
  }

  void returnToThis(String mode){
    if(!widget.connection.isConnected()){
      connectionError();
      return;
    }
    widget.connection.setParent(this);
    if(mode != null){
      setMode(mode);
    }else{
      widget.connection.sendModes();
    }
  }

  void receiveWelcome(Map<String, dynamic> message){
    return;
  }

  void receiveModes(Map<String, dynamic> message){
    List<String> modes = List<String>();
    for (var item in message['data']) {
      modes.add(item.toString());
    }
    modes.remove('mode');
    setState(() {
      widget.modes = modes;
    });
    print(widget.modes);
  }

  void connectionError(){
    Navigator.of(context).popUntil((route) => route.isFirst);
    Navigator.pushReplacement(context, MaterialPageRoute(builder: (BuildContext context) => ConnectionPage(connection: widget.connection)));
  }

  Icon getIconByMode(String mode){
    switch (mode) {
      case "clockanalog":
      case "clock":
        return Icon(Icons.query_builder);
      case "colors":
        return Icon(Icons.invert_colors);
      case "dvd":
        return Icon(Icons.insights);
      case "life":
        return Icon(Icons.scatter_plot);
      case "menu":
        return Icon(Icons.menu_open);
      case "pointmoving":
        return Icon(Icons.move_to_inbox);
      case "text":
        return Icon(Icons.format_size);
      case "draw":
        return Icon(Icons.create);
      case "image":
        return Icon(Icons.image);
      case "fourrow":
        return Icon(Icons.casino);
      case "snake":
        return Icon(Icons.timeline);
      case "tetris":
        return Icon(Icons.games);
      case "sound":
        return Icon(Icons.equalizer);
      case "fire":
        return Icon(Icons.whatshot);
      case "rain":
        return Icon(Icons.umbrella);
      case "twinkle":
        return Icon(Icons.grain);
      case "flappybird":
        return Icon(Icons.flight_takeoff);
      case "breakout":
        return Icon(Icons.code);
      case "video":
        return Icon(Icons.play_arrow);
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