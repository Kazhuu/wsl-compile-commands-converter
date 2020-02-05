import subprocess


def Settings( **kwargs ):
    print(kwargs['filename'])
    if kwargs[ 'language' ] == 'cfamily':
        print('cfamily')


def wsl_path(windows_path):
    completed_process = subprocess.run(['wslpath', '-a', windows_path], check=True)
    return completed_process.stdout

def main():
    command = "C:\\tools\\mingw64\\8.1.0\\bin\\c++.exe  -DVBOOT_FLASH_LAYOUT -D__DVPS__ -IC:/dev/product/product/controlboard/core0/../../../sw/firmware -IC:/ProgramData/chocolatey/lib/winpcap-developers-pack/tools/WpdPack/Include -IC:/dev/product/ext/googletest/googlemock/include -IC:/dev/product/ext/googletest/googlemock -IC:/dev/product/ext/googletest/googletest/include -IC:/dev/product/ext/googletest/googletest -isystem C:/tools/boost_1_62_0   -DGSL_THROW_ON_CONTRACT_VIOLATION -Wall -ftrack-macro-expansion=0 -Wno-stringop-truncation -Werror -std=gnu++14 -DTARGET_LITTLE_ENDIAN=1234 -D _SILENCE_TR1_NAMESPACE_DEPRECATION_WARNING -D _SILENCE_FPOS_SEEKPOS_DEPRECATION_WARNING   -g  -Og -fdata-sections -ffunction-sections -g3  -Wno-psabi -Wno-error=parentheses -Wno-parentheses  -faligned-new     -DGSL_THROW_ON_CONTRACT_VIOLATION -Wall -ftrack-macro-expansion=0 -Wno-stringop-truncation -Werror -std=gnu++14 -DTARGET_LITTLE_ENDIAN=1234 -D _SILENCE_TR1_NAMESPACE_DEPRECATION_WARNING -D _SILENCE_FPOS_SEEKPOS_DEPRECATION_WARNING -Wall -Wshadow -DGTEST_HAS_PTHREAD=1 -fexceptions -Wextra -Wno-unused-parameter -Wno-missing-field-initializers -o ext\\googletest\\build\\googlemock\\CMakeFiles\\gmock_main.dir\\__\\googletest\\src\\gtest-all.cc.obj -c C:\\dev\\product\\ext\\googletest\\googletest\\src\\gtest-all.cc"
    print(wsl_path('C:\\tools\\mingw64\\8.1.0\\bin\\c++.exe'))


if __name__ == '__main__':
    main()
