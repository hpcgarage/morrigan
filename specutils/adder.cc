#include <iostream>
#include <string>

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
    std::cout << "The sum is " << sum << std::endl;
    return 0;
}
