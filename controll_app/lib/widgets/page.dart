import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../connection.dart';
import '../settings.dart';

class DefaultPage extends StatelessWidget{

  ConnectionInterface? parent;
  String title;
  Widget child;
  FloatingActionButton? fab;
  Connection connection;
  bool showSettings;
  DefaultPage(this.title, this.child, this.connection, [this.fab, this.showSettings = true]);
  
  Widget build(BuildContext context){
    List<Widget> actions = [];
    if(showSettings){
      actions.add(IconButton(icon: Icon(Icons.settings), onPressed: (){
            Navigator.push(context, MaterialPageRoute(builder: (BuildContext context) => SettingsPage(connection: connection)));
          }));
    }
    if(fab == null){
      return Scaffold(
      appBar: AppBar(
        title: Text(title),
        actions: actions
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: new GestureDetector(
          behavior: HitTestBehavior.translucent,
          onTap: () {FocusScope.of(context).requestFocus(new FocusNode());},
          child: child
        )
      ),
    );
    }else{
      return Scaffold(
      appBar: AppBar(
        title: Text(title),
        actions: actions
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: child
      ),
      floatingActionButton: fab,
    );
    }
  }
}