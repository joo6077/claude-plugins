// 음성 대조용 감싸개 — 상태 저장소와 번역을 일부러 뺐다.
import 'package:app/core/theme/app_theme.dart';
import 'package:flutter/material.dart';

/// 검사가 돌리는 언어.
const hostLocales = [Locale('ko'), Locale('en')];

/// 언어마다 검사 전에 한 번 부른다.
Future<void> setUpHost(Locale locale) async {}

/// 위젯 하나를 테마만으로 감싼다.
Widget wrap(Widget child, {required double textScale, required Locale locale}) {
  return MaterialApp(
    debugShowCheckedModeBanner: false,
    theme: AppTheme.dark(),
    home: MediaQuery(
      data: MediaQueryData(textScaler: TextScaler.linear(textScale)),
      child: Material(type: MaterialType.transparency, child: child),
    ),
  );
}
