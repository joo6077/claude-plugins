// 옵션 목록 추출용: 로그 호출을 없앤다. 옵션 등록 결과에는 영향이 없다 (로그는 부작용만 있다)
#pragma once
#include <boost/log/trivial.hpp>
#include <iostream>
// 뱀부 2.9.1 부터 Log.hpp 가 BOOST_LOG_TRIVIAL 을 자기 로그 함수로 다시 정의한다. 그 함수(Log.cpp)는 링크하지 않아
// 정적 초기화 중에 빈 주소를 불러 죽는다 (2026-11-06 실측, 종료 코드 139). 먼저 넣어 두면 #pragma once 로 다시 안 들어온다
#if __has_include(<libslic3r/Log.hpp>)
#include <libslic3r/Log.hpp>
#endif
#undef BOOST_LOG_TRIVIAL
#define BOOST_LOG_TRIVIAL(lvl) if (true) {} else std::cerr
