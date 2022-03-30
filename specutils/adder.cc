#include <iostream>
#include <string>

int main() {
    int sum = 0;
    for (std::string line; std::getline(std::cin, line);) {
        try {
            sum += stoi(line);
        }
        catch (std::exception &err) {
            // nothing
        }
    }
    std::cout << sum << std::endl;
    return 0;
}
