import 'dart:async';
import 'dart:math' as math;
import 'dart:typed_data';

import 'package:controll_app/widgets/buttons.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:mic_stream/mic_stream.dart';
import 'package:smart_signal_processing/smart_signal_processing.dart';

import '../connection.dart';
import '../connectionPage.dart';
import '../widgets/page.dart';

class SoundModePage extends StatefulWidget {
  final Connection connection;

  SoundModePage({
    Key key,
    @required this.connection
  }): super(key: key);

  @override
  _SoundModePageState createState() => _SoundModePageState();
}

class _SoundModePageState extends State < SoundModePage > implements ConnectionInterface {
  bool active = true;
  int width = 20;
  int height = 15;
  int sensitivity = 30;
  List<double> values;
  Timer timer;

  StreamSubscription _dbSubscription;
  bool recording = false;
  bool started = false;
  int strokeType = 1;
  Stream<List<int>> stream;
  final AUDIO_FORMAT = AudioFormat.ENCODING_PCM_16BIT;
  final SAMPLE_RATE = 44100;
  //final LOGS = [math.log(2), math.log(3), math.log(4), math.log(5),math.log(6), math.log(7)];

  // Start listening to the stream

  @override
  Widget build(BuildContext context) {
    //final bloc = BlocProvider.of<PainterBloc>(context);

    if ( !recording && !started){
      started = true;
      startRecorder();
    }
    if (recording && (_dbSubscription == null)){
      _dbSubscription = stream.listen((samples) {
        var end_idx = math.pow(2,(math.log(samples.length)/math.log(2)).floor()).toInt();
        //var end_idx = math.pow(2, 5);

        // convert (Array<Int> to Float64List)
        var real = Float64List.fromList(samples.sublist(0,end_idx).map((v) => v.toDouble() ).toList());
        var imag = Float64List(real.length); // array of 0's for imaginary part

        final decayFactor = -10.0 / (real.length - 1);
        WinFunc.expMult(real, decayFactor, false, '0');

        // FFT transform inplace
        FFT.transform(real, imag);
        end_idx =  real.length~/2;
        real = real.sublist(0,end_idx);
        imag = imag.sublist(0,end_idx);
        // run again for fundamental frequencies
        //FFT.transform(real,imag);
        //end_idx = end_idx~/2;
        //real = real.sublist(0,end_idx);
        //imag = imag.sublist(0,end_idx);

        active = false;
        //for (var i = 0; i < values.length; i++) {
        //  values[i] = 0;
        //}
        for (var i=0; i < end_idx; i++){
          final magnitude = math.sqrt(real[i]*real[i]);

          // Specifically made for width of 15
          //values[(i*width/end_idx).floor()]+=magnitude;
          if(i >= 0 && i < 4){
            values[0]+=magnitude*5;
          }else if(i >= 4 && i < 6){
            values[1]+=magnitude*5;
          }else if(i >= 6 && i < 8){
            values[2]+=magnitude*5;
          }else if(i >= 8 && i < 10){
            values[3]+=magnitude*5;
          }else if(i >= 10 && i < 14){
            values[4]+=magnitude*2.5;
          }else if(i >= 14 && i < 19){
            values[5]+=magnitude*2;
          }else if(i >= 19 && i < 25){
            values[6]+=magnitude*1.6;
          }else if(i >= 25 && i < 33){
            values[7]+=magnitude*1.5;
          }else if(i >= 33 && i < 44){
            values[8]+=magnitude;
          }else if(i >= 44 && i < 59){
            values[9]+=magnitude/2;
          }else if(i >= 59 && i < 79){
            values[10]+=magnitude/2;
          }else if(i >= 79 && i < 106){
            values[11]+=magnitude/2;
          }else if(i >= 106 && i < 142){
            values[12]+=magnitude/4;
          }else if(i >= 142 && i < 192){
            values[13]+=magnitude/5;
          }else if(i >= 190 && i < 254){
            values[14]+=magnitude/6;
          }else if(i >= 254 && i < 339){
            values[15]+=magnitude/8;
          }else if(i >= 339 && i < 454){
            values[16]+=magnitude/5;
          }else if(i >= 454 && i < 607){
            values[17]+=magnitude/7;
          }else if(i >= 607 && i < 812){
            values[18]+=magnitude/8;
          }else if(i >= 812 && i < 1085){
            values[19]+=magnitude/10;
          }

          /*if(i >= 0 && i < 2){
            values[0]+=magnitude;
          }else if(i >= 2 && i < 3){
            values[1]+=magnitude;
          }else if(i >= 3 && i < 4){
            values[2]+=magnitude;
          }else if(i >= 4 && i < 5){
            values[3]+=magnitude;
          }else if(i >= 5 && i < 7){
            values[4]+=magnitude;
          }else if(i >= 7 && i < 9){
            values[5]+=magnitude;
          }else if(i >= 9 && i < 13){
            values[6]+=magnitude;
          }else if(i >= 13 && i < 17){
            values[7]+=magnitude;
          }else if(i >= 17 && i < 23){
            values[8]+=magnitude;
          }else if(i >= 23 && i < 30){
            values[9]+=magnitude;
          }else if(i >= 30 && i < 41){
            values[10]+=magnitude;
          }else if(i >= 41 && i < 54){
            values[11]+=magnitude;
          }else if(i >= 54 && i < 73){
            values[12]+=magnitude;
          }else if(i >= 73 && i < 97){
            values[13]+=magnitude;
          }else if(i >= 97 && i < 130){
            values[14]+=magnitude;
          }else if(i >= 130 && i < 174){
            values[15]+=magnitude;
          }else if(i >= 174 && i < 232){
            values[16]+=magnitude;
          }else if(i >= 232 && i < 311){
            values[17]+=magnitude;
          }else if(i >= 311 && i < 415){
            values[18]+=magnitude;
          }else if(i >= 415){
            values[19]+=magnitude;
          }*/
        }

        active = true;
        sendData();
      });
    }

    return DefaultPage("Sound Visualizer", GestureDetector(
      behavior: HitTestBehavior.translucent,
      onTap: () {
        FocusScope.of(context).requestFocus(new FocusNode());
      },
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: < Widget > [
          Center(
            child: GestureDetector(
            onTap: (){
              setState(() {
                active = !active;
              });
            },
            child:
            Container(
              decoration: BoxDecoration(
                color: (active)?Theme.of(context).accentColor:Colors.red,
                borderRadius: BorderRadius.circular(50)),
              width: 50,
              height: 50,
              child: Icon(
                (active)?Icons.mic:Icons.mic_off,
                color: Theme.of(context).primaryColor
              ),
            ),)
          ),
          Row(children: [
            Icon(Icons.mic),
            Text('Sensitivity: '),
            Expanded(child: Slider(
            value: sensitivity.toDouble(),
            min: 0,
            max: 100,
            divisions: 100,
            label: sensitivity.toString(),
            onChanged: (double value) {
              setState(() {
                sensitivity = value.round();
              });
            },
          )),
          IconButton(icon: Icon(Icons.settings_backup_restore), onPressed: (){
            setState(() {
              sensitivity = 30;
            });
          })
          ],),
          ControllerButtons(connection: widget.connection),
        ]
      ),
    ), widget.connection);
  }

  void sendData() {
    if(!active){
      return;
    }
    for (var i = 0; i < values.length; i++) {
      values[i] = math.min(height.toDouble(), values[i]*(sensitivity/10000)/height);
      //values[i] = math.min(height.toDouble(), values[i]*(sensitivity/10000)/height).round().toDouble();
    }
    Map < String, dynamic > settings = Map < String, dynamic > ();
    settings['values'] = values;
    widget.connection.sendModeSettings(settings);
    for (var i = 0; i < values.length; i++) {
      values[i] = 0;
    }
  }

  void receiveMode(Map < String, dynamic > message) {
    Navigator.of(context).pop(message['data']);
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
    widget.connection.setParent(this);
    values = new List<double>(width);
    for (var i = 0; i < values.length; i++) {
      values[i] = 0;
    }
    //timer = Timer.periodic(Duration(milliseconds: 20), (timer) {
    //  sendData();
    //});
    super.initState();
  }

  void startRecorder() {
    stream = microphone(
        audioSource: AudioSource.DEFAULT,
        sampleRate: SAMPLE_RATE,
        channelConfig: ChannelConfig.CHANNEL_IN_MONO,
        audioFormat: AUDIO_FORMAT);
    recording = true;
    print('recording!');
  }

  @override
  void dispose() {
    _dbSubscription.cancel();
    _dbSubscription = null;
    started = false;
    recording = false;
    timer.cancel();
    super.dispose();
  }

  int argmax(List<num> X){
  if (X.isEmpty){
    return null;
  }
  var _argmax = 0;
  var max = X[0];
  for (var i = 1; i < X.length; i++){
    if (max < X[i]){
      max = X[i];
      _argmax = i;
    }
  }
  return _argmax;
}

int PitchSpecralHPS(List<double> frequencies, int sample_rate){

  final iOrder = 4;
  final freq_min = 300;
  var freq_out = 0;

  final input_length = ((frequencies.length -1)/iOrder).floor();
  final afHps = frequencies.sublist(0,input_length);
  final k_min =  (freq_min*2*(frequencies.length-1)/sample_rate).round();

  for (var k=2; k <= iOrder; k++){ // iterate through multiples

    var idx = 0;
    for (var j=0; j<frequencies.length; j= j+k){  // down sample frequencies
      if (idx < input_length) {
        afHps[idx] = afHps[idx] + frequencies[j];
      }
      idx++;
    }
  }

  freq_out = argmax(afHps.sublist(k_min,input_length));

  // freq_out = (freq_out + k_min)*(sample_rate/2)/(frequencies.length - 1)

  return freq_out;
}

}