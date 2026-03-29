import 'package:app/shared/settings/presentation/pages/settings_page.dart';
import 'package:flutter/material.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

/// Fixture A: 완벽한 구현 — Expected: APPROVE
/// 이 파일은 shared/settings/presentation/pages/ 에 위치한다고 가정.

class SettingsPage extends HookConsumerWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeProvider);

    return Scaffold(
      body: ListView(
        children: [
          // UI-01: 테마 선택 행
          ListTile(
            title: const Text('테마'),
            trailing: Text(themeMode.name),
            onTap: () => ref.read(themeProvider.notifier).toggle(),
          ),
        ],
      ),
    );
  }
}
