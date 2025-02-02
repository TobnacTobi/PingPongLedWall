import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'connection.dart';
import 'modes.dart';
import 'widgets/buttons.dart';
import 'widgets/page.dart';

class ConnectionPage extends StatefulWidget {
  final String title = 'LED Wall Control';
  final Connection connection;

  ConnectionPage({Key? key, required this.connection})
      : super(key: key);

  @override
  _ConnectionPageState createState() => _ConnectionPageState();
}

class _ConnectionPageState extends State<ConnectionPage> implements ConnectionInterface{
  TextEditingController _addressController = TextEditingController();
  TextEditingController _portController = TextEditingController();
  List<String> received = List<String>.empty(growable: true);
  late SharedPreferences prefs;
  bool loading = false;

  @override
  Widget build(BuildContext context) {
    return DefaultPage(widget.title, 
    GestureDetector(
          behavior: HitTestBehavior.translucent,
          onTap: () {FocusScope.of(context).requestFocus(new FocusNode());},
          child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Form(child: Row(children: [
                Expanded(child: TextFormField(
                  controller: _addressController,
                  decoration: InputDecoration(labelText: 'Address'),
                )),
                SizedBox(width: 10),
                Expanded(child: TextFormField(
                  controller: _portController,
                  decoration: InputDecoration(labelText: 'Port'),
                  keyboardType: TextInputType.number,
                )),
                IconButton(
                  onPressed: (){_addressController.clear(); _portController.clear();},
                  icon: Icon(Icons.delete),
            ),
                ],
              )
            ),
            SizedBox(height: 10),
            SizedBox(width: double.infinity,
            child: ElevatedButton(
              onPressed: connect,
              child: Text('Connect'),
            )),
            //ControllerButtons(handleClicks),
            Column(
              children: received.map((e) => Text(e)).toList()
            ),
          ]
        ),
        ),
        widget.connection,
        null,
        false
    );
  }

  void handleClicks(String button){
    switch (button) {
      case 'up':
        widget.connection.sendUp();
        break;
      case 'down':
        widget.connection.sendDown();
        break;
      case 'left':
        widget.connection.sendLeft();
        break;
      case 'right':
        widget.connection.sendRight();
        break;
      case 'center':
        widget.connection.sendConfirm();
        break;
    }
    print(button);
  }





  void connect() async {
    EasyLoading.show(status: 'loading...');

    int? port;
    try {
      port = num.parse(_portController.text) as int?;
    } catch (e) {
      //print('Could not parse port to num.');
    }
    bool result = await widget.connection.connect(_addressController.text, port);
    await prefs.setString('address', _addressController.text);
    await prefs.setString('port', _portController.text);
    EasyLoading.dismiss();
    if(!result){
      EasyLoading.showError('Could not connect to LED Wall');
    }
  }

  void receiveWelcome(Map<String, dynamic> message){
    widget.connection.sendModes();
  }

  void receiveModes(Map<String, dynamic> message){
    print(message);
    List<String> modes = List<String>.empty(growable: true);
    for (var item in message['data']) {
      modes.add(item.toString());
    }
    Navigator.of(context).popUntil((route) => route.isFirst);
    Navigator.pushReplacement(context, MaterialPageRoute(builder: (BuildContext context) => ModesPage(connection: widget.connection, modes: modes)));
  }

  void receiveMode(Map<String, dynamic> message){
    print('Cant interpret mode on connectionPage.');
  }
  
  void connectionError(){
    EasyLoading.showError('Connection Error');
  }

  @override
  void initState() {
    loadDefaults();
    widget.connection.setParent(this);
    super.initState();
    //this.connect();
  }

  
  void loadDefaults() async {
    prefs = await SharedPreferences.getInstance();
    _addressController.text = prefs.getString('address')!;
    _portController.text = prefs.getString('port')!;
  }

  @override
  void dispose() {
    super.dispose();
  }
}