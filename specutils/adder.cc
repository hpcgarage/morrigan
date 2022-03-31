#include <iostream>
#include <string>
#include <cstdlib>

void ariel_enable() {
    printf("ARIEL-CLIENT: Library enabled.\n");
}

int main() {
    ariel_enable();
    int sum = 0;
    for (std::string line; std::getline(std::cin, line);) {
        try {
            sum += stoi(line);
        }
        catch (std::exception &err) {
            // nothing
        }
    }

    if(const char* env_p = std::getenv("MYENVVAR")) {
        std::cout << "The value of MYENVVAR is " << env_p << std::endl;
    }
    else {
        std::cout << "MYENVVAR not found" << std::endl;
    }

    std::cout << "The sum is " << sum << std::endl;
    std::cerr << "ERROR: The sum is " << sum << std::endl;
    return 0;
}
