// 슬라이서 태그 소스의 옵션 등록부를 그대로 초기화해 설정 키를 판정한다.
//   dump      : 등록된 옵션 키와 별칭을 출력한다
//   classify  : 표준 입력의 키를 JSON 불러오기와 같은 순서(handle_legacy → 등록부 확인)로 판정한다
//   presets   : 프리셋 종류별 기본 설정의 키를 출력한다. 설정 가져오기는 이 목록에 없는 키를 지운다 (remove_invalid_keys)
//   values    : 표준 입력의 "키<TAB>값" 을 실제 역직렬화 경로(set_deserialize)에 넣어 값이 받아들여지는지 판정한다
#include "libslic3r/PrintConfig.hpp"
#include "libslic3r/PresetBundle.hpp"
#include <iostream>
#include <string>

using namespace Slic3r;

int main(int argc, char **argv)
{
    const std::string mode = argc > 1 ? argv[1] : "dump";
    if (mode == "dump") {
        for (const auto &entry : print_config_def.options) {
            std::cout << "canonical\t" << entry.first << '\n';
            for (const auto &alias : entry.second.aliases)
                std::cout << "alias\t" << alias << '\t' << entry.first << '\n';
            // enum 옵션이 받아들이는 문자열 — 역직렬화가 이 표로 값을 찾는다
            const ConfigOptionDef &def = entry.second;
            if ((def.type == coEnum || def.type == coEnums) && def.enum_keys_map != nullptr)
                for (const auto &value : *def.enum_keys_map)
                    std::cout << "enum\t" << entry.first << '\t' << value.first << '\n';
        }
        return 0;
    }
    if (mode == "classify") {
        std::string key;
        while (std::getline(std::cin, key)) {
            if (key.empty()) continue;
            t_config_option_key resolved = key;
            std::string value = "0";
            PrintConfigDef::handle_legacy(resolved, value);
            if (resolved.empty())       std::cout << "dropped\t" << key << '\n';
            else if (resolved == key)   std::cout << "accepted\t" << key << '\n';
            else                        std::cout << "renamed\t" << key << '\t' << resolved << '\n';
        }
        return 0;
    }
    if (mode == "values") {
        // set_deserialize_nothrow 와 같은 순서: handle_legacy(키·값 둘 다 바뀔 수 있다) → 역직렬화 → 대체 여부
        std::string line;
        while (std::getline(std::cin, line)) {
            const size_t tab = line.find('\t');
            if (tab == std::string::npos) continue;
            const std::string key = line.substr(0, tab), value = line.substr(tab + 1);
            t_config_option_key resolved_key = key;
            std::string resolved_value = value;
            PrintConfigDef::handle_legacy(resolved_key, resolved_value);
            std::string verdict;
            if (resolved_key.empty()) {
                verdict = "dropped";
            } else {
                DynamicPrintConfig config;
                ConfigSubstitutionContext context(ForwardCompatibilitySubstitutionRule::Enable);
                try {
                    config.set_deserialize(resolved_key, resolved_value, context);
                    verdict = context.substitutions.empty() ? "accepted" : "substituted";
                } catch (const std::exception &) {
                    verdict = "error";
                }
            }
            std::cout << verdict << '\t' << key << '\t' << value << '\t' << resolved_key << '\t' << resolved_value << '\n';
        }
        return 0;
    }
    if (mode == "presets") {
        PresetBundle bundle;
        const std::pair<const char *, const PresetCollection *> collections[] = {
            {"process", &bundle.prints}, {"filament", &bundle.filaments}, {"machine", &bundle.printers}};
        for (const auto &[type, collection] : collections)
            for (const std::string &key : collection->default_preset().config.keys())
                std::cout << type << '\t' << key << '\n';
        return 0;
    }
    std::cerr << "usage: option_key_probe dump|classify|presets|values\n";
    return 2;
}
