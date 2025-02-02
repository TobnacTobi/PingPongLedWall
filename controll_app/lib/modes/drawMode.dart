import 'dart:convert';
import 'package:zoom_widget/zoom_widget.dart';
import 'package:controll_app/widgets/buttons.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';
import 'package:zoom_widget/zoom_widget.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../connection.dart';
import '../connectionPage.dart';
import '../widgets/page.dart';
int currentpans = 0;
class DrawModePage extends StatefulWidget {
  final Connection connection;
  final int sizex = 20;
  final int sizey = 15;

  

  DrawModePage({
    Key? key,
    required this.connection
  }): super(key: key);

  @override
  _DrawModePageState createState() => _DrawModePageState();
}

class _DrawModePageState extends State < DrawModePage > implements ConnectionInterface {
  List < String > received = List<String>.empty(growable: true);
  SharedPreferences? prefs;
  Color _selectedColor = Colors.white;
  String? _selectedAction = 'draw'; // draw, fill
  List < List < LEDPoint >> _points = < List < LEDPoint >> [];

  @override
  Widget build(BuildContext context) {
    return DefaultPage("Draw",
      Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Builder(builder: (BuildContext context) {
            return GestureDetector(
              onTapDown: (details) {
                RenderBox object = context.findRenderObject() as RenderBox;
                Offset _localPosition = object.globalToLocal(details.globalPosition);
                int x = (_localPosition.dx / ((MediaQuery.of(context).size.width - 30) / widget.sizex)).floor();
                int y = (_localPosition.dy / ((MediaQuery.of(context).size.width) / widget.sizex)).floor();
                if (x >= 0 && y >= 0 && x < widget.sizex && y < widget.sizey) {
                  switch (_selectedAction) {
                    case 'fill':
                      fillRecursively(x, y);
                      sendPoints();
                      break;
                    case 'draw':
                      if (_points[x][y].color != _selectedColor) {
                        _points[x][y].color = _selectedColor;
                        sendPoint(x, y);
                      }
                      break;
                    default:
                  }
                }
                setState(() {
                  _points = List.from(_points);
                });
              },
              onPanUpdate: (details) {
                RenderBox object = context.findRenderObject() as RenderBox;
                Offset _localPosition = object.globalToLocal(details.globalPosition);
                int x = (_localPosition.dx / ((MediaQuery.of(context).size.width - 30) / widget.sizex)).floor();
                int y = (_localPosition.dy / ((MediaQuery.of(context).size.width) / widget.sizex)).floor();
                if (x >= 0 && y >= 0 && x < widget.sizex && y < widget.sizey) {
                  switch (_selectedAction) {
                    case 'draw':
                      if (_points[x][y].color != _selectedColor) {
                        _points[x][y].color = _selectedColor;
                        sendPoint(x, y);
                      }
                      break;
                    default:
                  }
                }
                setState(() {
                  _points = List.from(_points);
                });
              },
              child: Center(
                child: CustomPaint(
                  painter: LEDPainter(widget.sizex, widget.sizey, _points),
                  child: Container(
                    width: MediaQuery.of(context).size.width,
                    height: (MediaQuery.of(context).size.width / widget.sizex) * widget.sizey,
                    //color: Colors.red
                  ), )
              ),
              );
          }),

          Row(children: [
            ElevatedButton(onPressed: () {
              showDialog(context: context, builder: (_) => getAlertDialog());
            }, child: Text('Color', style: TextStyle(color: Colors.black, backgroundColor: _selectedColor), )),
            SizedBox(width: 10),
            DropdownButton(items: [
              DropdownMenuItem(child: Row(children: [Icon(Icons.create), Text('Draw')], ), value: 'draw'),
              DropdownMenuItem(child: Row(children: [Icon(Icons.format_color_fill), Text('Fill')], ), value: 'fill'),
            ], value: _selectedAction, onChanged: (dynamic v) {
              setState(() {
                _selectedAction = v;
              });
            }),
            IconButton(
              onPressed: () {
                initPoints();
                sendPoints();
              },
              icon: Icon(Icons.delete),
            )
          ], ),
          Row(children: [
            buildColorButton(Colors.white), buildColorButton(Colors.black), buildColorButton(Colors.green), buildColorButton(Colors.blue), buildColorButton(Colors.red), buildColorButton(Colors.yellow), buildColorButton(Colors.orange),
          ], ),
          Row(children: [
            buildColorButton(Colors.purple), buildColorButton(Colors.pink), buildColorButton(Colors.lime), buildColorButton(Colors.brown), buildColorButton(Colors.cyan), buildColorButton(Colors.teal), buildColorButton(Colors.deepOrange),
          ], ),
          
        ], ), widget.connection);
  }

  Widget buildColorButton(Color c) {
    return ButtonTheme(
      minWidth: 50.0,
      height: 30.0,
      child: TextButton(
        onPressed: () {
          setState(() {
            _selectedColor = c;
          });
        },
        child: SizedBox(width: 10),
        //style: TextStyle(color: c),
        //shape: CircleBorder(side: BorderSide.none),
      ),
    );
  }

  sendPoint(int x, int y) {
    Map < String, dynamic > settings = Map < String, dynamic > ();
    List < int > point = [x, y, _points[x][y].color.red, _points[x][y].color.green, _points[x][y].color.blue];
    settings['point'] = point;
    widget.connection.sendModeSettings(settings);
  }

  void sendPoints() {
    Map < String, dynamic > settings = Map < String, dynamic > ();
    List < List < List < int >>> points = [];
    for (List < LEDPoint > pointsx in _points) {
      List < List < int >> tmpy = [];
      for (LEDPoint point in pointsx) {
        tmpy.add([point.color.red, point.color.green, point.color.blue]);
      }
      points.add(tmpy);
    }
    settings['points'] = points;
    widget.connection.sendModeSettings(settings);
  }

  void receiveMode(Map < String, dynamic > message) {
    Navigator.of(context).pop(message['data']);
  }

  void receiveWelcome(Map < String, dynamic > message) {
    return;
  }

  void receiveModes(Map < String, dynamic > message) {
    return;
  }

  void connectionError() {
    Navigator.of(context).popUntil((route) => route.isFirst);
    Navigator.pushReplacement(context, MaterialPageRoute(builder: (BuildContext context) => ConnectionPage(connection: widget.connection)));
  }

  void fillRecursively(int x, int y, [Color? compareto = null]) {
    if (x < 0 || y < 0 || x > widget.sizex - 1 || y > widget.sizey - 1 || _points[x][y].color == _selectedColor || (compareto != null && _points[x][y].color != compareto)) {
      return;
    }
    if (compareto == null) {
      compareto = _points[x][y].color;
    }
    _points[x][y].color = _selectedColor;
    //sendPoint(x, y);
    fillRecursively(x + 1, y, compareto);
    fillRecursively(x - 1, y, compareto);
    fillRecursively(x, y + 1, compareto);
    fillRecursively(x, y - 1, compareto);
  }

  Widget getAlertDialog() {
    Color currentColor = _selectedColor;

    return AlertDialog(
      title: const Text('Pick a color!'),
        content: SingleChildScrollView(
          child: ColorPicker(
            pickerColor: currentColor,
            onColorChanged: (c) {
              setState(() {
                currentColor = c;
              });
            },
            showLabel: true, displayThumbColor: true,
            pickerAreaHeightPercent: 0.8,
          ),
        ),
        actions: < Widget > [
          TextButton(
            child: const Text('Set'),
              onPressed: () {
                setState(() {
                  _selectedColor = currentColor;
                });
                Navigator.of(context).pop();
              },
          ),
        ],
    );
  }

  initPoints() {
    _points = [];
    for (var x = 0; x < widget.sizex; x++) {
      List < LEDPoint > tmp = < LEDPoint > [];
      for (var y = 0; y < widget.sizey; y++) {
        tmp.add(LEDPoint(x, y, Colors.black));
      }
      _points.add(tmp);
    }
    setState(() {
      _points = List.from(_points);
    });
  }

  @override
  void initState() {
    widget.connection.setParent(this);
    initPoints();
    super.initState();
  }
  @override
  void dispose() {
    super.dispose();
  }
}

class LEDPoint {
  final int x;
  final int y;
  Color color;
  LEDPoint(this.x, this.y, this.color);
}

class LEDPainter extends CustomPainter {
  final int sizex;
  final int sizey;
  final List < List < LEDPoint >> pointss;

  LEDPainter(this.sizex, this.sizey, this.pointss): super();

  @override
  void paint(Canvas canvas, Size size) {
    double recwidth = size.width / sizex;
    double recheight = size.height / sizey;
    for (List < LEDPoint > points in pointss) {
      for (LEDPoint point in points) {
        Paint p = Paint()..color = point.color..strokeWidth = 0;
        canvas.drawCircle(Offset(point.x * recwidth, point.y * recheight), (recwidth + recheight) / 4, p);
        //canvas.drawRect(Offset(point.x * recwidth, point.y * recheight) & Size(recwidth, recheight), p);
      }
    }

    //final Paint linePaint = Paint()
    //  ..color = Colors.black
    //  ..strokeWidth = 1;
    //for (var x = 0; x < sizex; x++) {
    //  for (var y = 0; y < sizey; y++) {
    //    canvas.drawLine(Offset(0,y*recheight), Offset(size.width, y*recheight), linePaint);
    //    canvas.drawLine(Offset(x*recwidth,0), Offset(x*recwidth, size.height), linePaint);
    //  }
    //}
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;

}