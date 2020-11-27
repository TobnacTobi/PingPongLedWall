

import 'package:flutter/cupertino.dart';
import 'package:path_drawing/path_drawing.dart';

import '../connection.dart';

class ControllerButtons extends StatelessWidget{

  // takes String of [up, down, left, right, center]
  Connection connection;
  ControllerButtons({this.connection});

  @override
  Widget build(BuildContext context){
    return Stack(
          children: <Widget>[
            _getClippedImage(
              clipper: _Clipper(
                svgPath: svgUP,
                offset: Offset(45, -14),
              ),
              image: 'assets/whole_button.png',
              onClick: (){_handleClick('up');},
            ),
            _getClippedImage(
              clipper: _Clipper(
                svgPath: svgDOWN,
                offset: Offset(65, 275),
              ),
              image: 'assets/whole_button.png',
              onClick: (){_handleClick('down');},
            ),
            _getClippedImage(
              clipper: _Clipper(
                svgPath: svgLEFT,
                offset: Offset(-10, 50),
              ),
              image: 'assets/whole_button.png',
              onClick: (){_handleClick('left');},
            ),
            _getClippedImage(
              clipper: _Clipper(
                svgPath: svgRIGHT,
                offset: Offset(280, 50),
              ),
              image: 'assets/whole_button.png',
              onClick: (){_handleClick('right');},
            ),
            _getClippedImage(
              clipper: _Clipper(
                svgPath: svgCENTER,
                offset: Offset(80, 80),
              ),
              image: 'assets/whole_button.png',
              onClick: (){_handleClick('center');},
            ),
            ]);
  }

    void _handleClick(String button){
    switch (button) {
      case 'up':
        connection.sendUp();
        break;
      case 'down':
        connection.sendDown();
        break;
      case 'left':
        connection.sendLeft();
        break;
      case 'right':
        connection.sendRight();
        break;
      case 'center':
        connection.sendConfirm();
        break;
    }
    print(button);
  }

  Widget _getClippedImage({
      _Clipper clipper,
      String image,
      void Function() onClick, }) {
        clipper.setImageScale(1000, 1000);
        return ClipPath(
          clipper: clipper,
          child: GestureDetector(
            onTap: onClick,
            child: Image.asset('assets/whole_button.png'),
          ),
        );
    }

}

class _Clipper extends CustomClipper<Path> {
      _Clipper({this.svgPath, this.offset = Offset.zero, this.imagewidth, this.imageheight});

      String svgPath;
      Offset offset;
      double imagewidth;
      double imageheight;
      @override
      Path getClip(Size size) {
        var path = parseSvgPathData(svgPath);
        if(imagewidth != null && imageheight != null){
          final Matrix4 matrix4 = Matrix4.identity();
          matrix4.scale(size.width / imagewidth, size.height / imageheight);
          path = path.transform(matrix4.storage);
        }

        return path.shift(offset);
      }

      @override
      bool shouldReclip(CustomClipper oldClipper) {
        return false;
      }

      void setImageScale(double w, double h){
        this.imagewidth = w;
        this.imageheight = h;
      }
    }
/*
const svgUP = "M87 1H0.5V29H87V1Z";
const svgDOWN = "M32 0.5H0.5V80.5H32V0.5Z";
const svgLEFT = "M0.5 31V0.5H87V31H0.5Z";
const svgRIGHT = "M44 0.5H0.5V73H44V0.5Z";*/

const svgUP = "M170 271L1 119C78 79.3333 263.8 0.2 391 1C518.2 1.8 670.667 92.6667 731 138C703.333 200.667 637.2 315 594 271C540 216 493 218 391 207C309.4 198.2 209.667 246 170 271Z";
const svgDOWN = "M1 131L129 1C177.333 31 294 91 374 91C454 91 540.667 38.3333 574 12L700 150C652 190.667 513.2 271.6 342 270C170.8 268.4 43.3333 176.667 1 131Z";
const svgLEFT = "M302 182.5C248.333 132.167 136.9 25.4 120.5 1C81.3333 47.8333 2.6 187.7 1 372.5C-0.6 557.3 107 697.167 161 744C208 701.667 297.8 613.2 281 598C260 579 225.5 501.5 214 388.5C204.8 298.1 268.833 213.5 302 182.5Z";
const svgRIGHT = "M1.5 124.5L148.5 1C196.5 53.5 292 195.6 290 344C288 492.4 194.833 635.833 148.5 689L8 568C33.1667 527.667 84.5 422.8 88.5 326C92.5 229.2 32.1667 151.333 1.5 124.5Z";
const svgCENTER = "M76 476C-65.9999 324 23.8333 125 97.5 63.5C177.333 19 329.414 -61.5927 474 85.5C647 261.5 481 461 462.5 484.5C444 508 218 628 76 476Z";