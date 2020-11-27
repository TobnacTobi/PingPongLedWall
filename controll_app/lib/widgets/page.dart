import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../connection.dart';

class DefaultPage extends StatelessWidget{

  String title;
  Widget child;
  FloatingActionButton fab;
  DefaultPage(this.title, this.child, [this.fab]);
  
  Widget build(BuildContext context){
    if(fab == null){
      return Scaffold(
      appBar: AppBar(
        title: Text(title),
        actions: [
          IconButton(icon: Icon(Icons.settings), onPressed: openSettings)
        ],
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
        actions: [
          IconButton(icon: Icon(Icons.settings), onPressed: openSettings)
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: child
      ),
      floatingActionButton: fab, // This trailing comma makes auto-formatting nicer for build methods.
    );
    }
  }

  openSettings(){
    print("openSettings pressed");
  }
}