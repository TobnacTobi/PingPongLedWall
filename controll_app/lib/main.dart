import 'package:controll_app/connection.dart';
import 'package:flutter/material.dart';
import 'connectionPage.dart';
import 'package:flutter_easyloading/flutter_easyloading.dart';

import 'modes/drawMode.dart';
import 'modes/textMode.dart';

void main() {
  runApp(MyApp());
  configLoading();
}

class MyApp extends StatelessWidget {
  final connection = Connection();
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LED Wall Control',
      theme: ThemeData(
        brightness: Brightness.dark,
        primarySwatch: Colors.deepOrange,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: ConnectionPage(connection: connection),
      //home: DrawModePage(connection: connection),
      builder: EasyLoading.init(),
    );
  }
}

void configLoading() {
  EasyLoading.instance
    ..displayDuration = const Duration(milliseconds: 2000)
    ..indicatorType = EasyLoadingIndicatorType.threeBounce
    ..loadingStyle = EasyLoadingStyle.dark
    ..indicatorSize = 45.0
    ..radius = 10.0
    ..progressColor = Colors.yellow
    ..backgroundColor = Colors.green
    ..indicatorColor = Colors.yellow
    ..textColor = Colors.yellow
    ..maskColor = Colors.blue.withOpacity(0.5)
    ..userInteractions = true
    ..dismissOnTap = false;
}

