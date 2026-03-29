import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:flutter/material.dart';

part 'theme_provider.g.dart';

/// LG-01: 테마 변경 시 Provider 상태 업데이트
@riverpod
class Theme extends _$Theme {
  @override
  ThemeMode build() => ThemeMode.system;

  void toggle() {
    state = state == ThemeMode.dark ? ThemeMode.light : ThemeMode.dark;
  }
}
