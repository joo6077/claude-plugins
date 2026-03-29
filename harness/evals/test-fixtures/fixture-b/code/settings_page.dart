import 'package:flutter/material.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

/// Fixture B: 1개 FAIL — Expected: REJECT (LG-01 미구현)
/// Provider가 없다. UI만 하드코딩.

class SettingsPage extends HookConsumerWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      body: ListView(
        children: [
          // UI-01: 테마 선택 행 (표시는 됨)
          ListTile(
            title: const Text('테마'),
            trailing: const Text('System'),
            // LG-01 FAIL: Provider 없음, onTap 없음
          ),
        ],
      ),
    );
  }
}
