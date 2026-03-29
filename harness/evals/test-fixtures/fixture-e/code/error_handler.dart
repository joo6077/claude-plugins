import 'package:riverpod_annotation/riverpod_annotation.dart';

/// Fixture E: 주석 함정 — Expected: REJECT
/// 주석에 "처리 완료"라고만 써 있고 실제 errorProvider 호출 없음.

class SomeNotifier {
  Future<void> fetchData() async {
    try {
      // final result = await repository.getData();
      // state = result;
    } catch (e) {
      // 에러 처리 완료
      // TODO: errorProvider 연결
    }
  }
}
