import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'connection.dart';
import 'connectionPage.dart';
import 'widgets/page.dart';
import 'modes/defaultMode.dart';

class SettingsPage extends StatefulWidget {
  final Connection connection;

  SettingsPage({
    Key key,
    @required this.connection,
  }): super(key: key);

  @override
  _SettingsPageState createState() => _SettingsPageState();
}

class _SettingsPageState extends State < SettingsPage > implements ConnectionInterface {
  SharedPreferences prefs;
  int _brightness = 50;
  int _size = 10;
  int _speed = 10;

  @override
  Widget build(BuildContext context) {
    return DefaultPage("Settings",
      Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(children: [
            Icon(Icons.lightbulb),
            Text(' Brightness: '),
            Expanded(child: Slider(
            value: _brightness.toDouble(),
            min: 0,
            max: 100,
            divisions: 100,
            label: _brightness.toString(),
            onChangeEnd: (double v){
              sendSettings();
            },
            onChanged: (double value) {
              setState(() {
                _brightness = value.round();
                sendSettings();
              });
            },
          )),
          IconButton(icon: Icon(Icons.settings_backup_restore), onPressed: (){
            setState(() {
              _brightness = 50;
              sendSettings();
            });
          })
          ],),
          Row(children: [
            Icon(Icons.fast_forward),
            Text(' Speed: '),
            Expanded(child: Slider(
            value: _speed.toDouble(),
            min: 1,
            max: 100,
            divisions: 100,
            label: _speed.toString(),
            onChangeEnd: (double v){
              sendSettings();
            },
            onChanged: (double value) {
              setState(() {
                _speed = value.round();
              });
            },
          )),
          IconButton(icon: Icon(Icons.settings_backup_restore), onPressed: (){
            setState(() {
              _speed = 10;
              sendSettings();
            });
          })
          ],),
          Row(children: [
            Icon(Icons.aspect_ratio),
            Text(' Size: '),
            Expanded(child: Slider(
            value: _size.toDouble(),
            min: 1,
            max: 100,
            divisions: 100,
            label: _size.toString(),
            onChangeEnd: (double v){
              sendSettings();
            },
            onChanged: (double value) {
              setState(() {
                _size = value.round();
              });
            },
          )),
          IconButton(icon: Icon(Icons.settings_backup_restore), onPressed: (){
            setState(() {
              _size = 10;
              sendSettings();
            });
          })
          ],),
          SizedBox(width: double.infinity,
            child: RaisedButton(
              onPressed: sendDisconnect,
              child: Text('Disconnect'),
            )),
          Text("Connection Nr: "+widget.connection.connection_number.toString())
        ],
      ),
      widget.connection,
      null,
      false
    );
  }

  void sendSettings() async {
    Map<String, dynamic> settings = {'size':_size, 'speed': _speed, 'brightness': _brightness};
    await widget.connection.sendSettings(settings);
    await prefs.setInt('brightness', _brightness);
    await prefs.setInt('size', _size);
    await prefs.setInt('speed', _speed);
  }

  void sendDisconnect(){
    widget.connection.close();
    Navigator.of(context).popUntil((route) => route.isFirst);
    Navigator.pushReplacement(context, MaterialPageRoute(builder: (BuildContext context) => ConnectionPage(connection: widget.connection)));
  }

  void receiveMode(Map < String, dynamic > message) {
    print(message);
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
    //widget.connection.setParent(this);
    loadDefaults();
    super.initState();
  }
  void loadDefaults() async {
    prefs = await SharedPreferences.getInstance();
    setState(() {
      _brightness = prefs.getInt('brightness')??50;
      _size = prefs.getInt('size')??10;
      _speed = prefs.getInt('speed')??10;
    });
  }

  @override
  void dispose() {
    super.dispose();
  }
}