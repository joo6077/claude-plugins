// 핏팰 복사본 측정용 감싸개 — 앱 테마 · 상태 저장소 · 번역을 붙인다.
import 'package:app/catalog/stage/catalog_session_scope.dart';
import 'package:app/core/i18n/strings.g.dart';
import 'package:app/core/theme/app_theme.dart';
import 'package:flutter/material.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

/// 검사가 돌리는 언어.
const hostLocales = [Locale('ko'), Locale('en')];

/// 언어마다 검사 전에 한 번 부른다.
Future<void> setUpHost(Locale locale) async {
  await LocaleSettings.setLocaleRaw(locale.languageCode);
}

/// 위젯 하나를 앱과 같은 환경으로 감싼다.
Widget wrap(Widget child, {required double textScale, required Locale locale}) {
  return ProviderScope(
    overrides: catalogSessionOverrides(),
    child: TranslationProvider(
      child: MaterialApp(
        debugShowCheckedModeBanner: false,
        theme: AppTheme.dark(),
        home: Builder(
          builder: (context) => MediaQuery(
            data: MediaQuery.of(context).copyWith(
              textScaler: TextScaler.linear(textScale),
            ),
            child: Material(type: MaterialType.transparency, child: child),
          ),
        ),
      ),
    ),
  );
}
