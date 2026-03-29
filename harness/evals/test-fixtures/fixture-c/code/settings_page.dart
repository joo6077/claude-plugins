import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Fixture C: Anti-pattern 위반 — Expected: REJECT (AP-01 StatefulWidget)
/// 기능은 완벽하지만 StatefulWidget 사용.

class SettingsPage extends ConsumerStatefulWidget {
  const SettingsPage({super.key});

  @override
  ConsumerState<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends ConsumerState<SettingsPage> {
  @override
  Widget build(BuildContext context) {
    final themeMode = ref.watch(themeProvider);

    return Scaffold(
      body: ListView(
        children: [
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
