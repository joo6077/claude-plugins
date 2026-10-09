// 측정용 시험 위젯 — 일부러 망가뜨린 것과 정상인 것을 짝으로 둔다.
import 'package:flutter/material.dart';

/// 폭 120 안의 줄에 글자를 감싸지 않고 넣는다 — 긴 글자에서 넘친다.
class OverflowProbe extends StatelessWidget {
  /// [label] 은 줄에 넣을 글자.
  const OverflowProbe({super.key, this.label = '확인'});

  /// 줄에 넣을 글자.
  final String label;

  @override
  Widget build(BuildContext context) =>
      SizedBox(width: 120, child: Row(children: [Text(label)]));
}

/// 글자만 8 아래로 내려 아이콘과 가운데가 어긋난다.
class IconProbeBad extends StatelessWidget {
  /// [label] 은 아이콘 옆 글자.
  const IconProbeBad({super.key, this.label = '라벨'});

  /// 아이콘 옆 글자.
  final String label;

  @override
  Widget build(BuildContext context) => Row(
    mainAxisSize: MainAxisSize.min,
    children: [
      const Icon(Icons.star, size: 16),
      Padding(padding: const EdgeInsets.only(top: 8), child: Text(label)),
    ],
  );
}

/// 아이콘과 글자를 줄 가운데에 맞춘다.
class IconProbeGood extends StatelessWidget {
  /// [label] 은 아이콘 옆 글자.
  const IconProbeGood({super.key, this.label = '라벨'});

  /// 아이콘 옆 글자.
  final String label;

  @override
  Widget build(BuildContext context) => Row(
    mainAxisSize: MainAxisSize.min,
    children: [
      const Icon(Icons.star, size: 16),
      const SizedBox(width: 4),
      Text(label),
    ],
  );
}

/// 켜지면 높이가 30 에서 40 으로 바뀐다.
class StateProbe extends StatelessWidget {
  /// [active] 는 켜짐 여부.
  const StateProbe({super.key, this.active = false});

  /// 켜짐 여부.
  final bool active;

  @override
  Widget build(BuildContext context) =>
      SizedBox(width: 40, height: active ? 40 : 30);
}

/// 20 × 20 짜리 누를 수 있는 칸 — 터치 영역이 너무 작다.
class TapSmallProbe extends StatelessWidget {
  /// 기본 생성자.
  const TapSmallProbe({super.key});

  @override
  Widget build(BuildContext context) => Semantics(
    button: true,
    label: '작은 칸',
    onTap: () {},
    child: const SizedBox(width: 20, height: 20),
  );
}

/// 48 × 48 짜리 누를 수 있는 칸.
class TapBigProbe extends StatelessWidget {
  /// 기본 생성자.
  const TapBigProbe({super.key});

  @override
  Widget build(BuildContext context) => Semantics(
    button: true,
    label: '큰 칸',
    onTap: () {},
    child: const SizedBox(width: 48, height: 48),
  );
}
