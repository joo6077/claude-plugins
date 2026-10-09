// 핏팰 복사본 측정용 놀이터 감싸개 — 앱 테마 · 상태 저장소 · 번역을 붙인다.
import 'package:app/catalog/stage/catalog_session_scope.dart';
import 'package:app/core/i18n/strings.g.dart';
import 'package:app/core/theme/app_theme.dart';
import 'package:flutter/material.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

/// 놀이터 화면 전체를 앱과 같은 환경으로 감싼다.
Widget appWrap(Widget child) {
  LocaleSettings.setLocaleRawSync('ko');
  return ProviderScope(
    overrides: catalogSessionOverrides(),
    child: TranslationProvider(
      child: MaterialApp(
        debugShowCheckedModeBanner: false,
        theme: AppTheme.dark(),
        home: child,
      ),
    ),
  );
}
