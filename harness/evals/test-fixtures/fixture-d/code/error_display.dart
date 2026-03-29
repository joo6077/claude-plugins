import 'package:flutter/material.dart';

/// Fixture D: 관대함 함정 — Expected: REJECT
/// 계약은 "스낵바"인데 Toast로 구현.
/// 기능적으로 동일하지만 계약 조건과 다름.

void showError(BuildContext context, String message) {
  // UI-01 FAIL: 계약은 "스낵바" → 실제는 Toast
  showToast(context, message);
}

void showToast(BuildContext context, String message) {
  final overlay = Overlay.of(context);
  final entry = OverlayEntry(
    builder: (context) => Positioned(
      bottom: 50,
      left: 20,
      right: 20,
      child: Material(
        borderRadius: BorderRadius.circular(8),
        color: Colors.black87,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Text(message, style: const TextStyle(color: Colors.white)),
        ),
      ),
    ),
  );
  overlay.insert(entry);
  Future.delayed(const Duration(seconds: 2), entry.remove);
}
