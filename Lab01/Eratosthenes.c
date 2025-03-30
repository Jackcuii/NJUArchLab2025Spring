#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX 1000000

void sieve_of_eratosthenes(bool is_prime[], int limit) {
    for (int i = 0; i <= limit; i++) {
        is_prime[i] = true;
    }
    is_prime[0] = false;
    is_prime[1] = false;
    for (int i = 2; i * i <= limit; i++) {
        if (is_prime[i]) {
            for (int j = i * i; j <= limit; j += i) {
                is_prime[j] = false;
            }
        }
    }
}

int main() {
    bool *is_prime = (bool *)malloc((MAX + 1) * sizeof(bool));
    if (is_prime == NULL) {
        return 1;
    }
    sieve_of_eratosthenes(is_prime, MAX);
    int count = 0;
    for (int i = 2; i <= MAX; i++) {
        if (is_prime[i]) {
            count++;
        }
    }
    printf("%d\n", count);
    free(is_prime);
    return 0;
}
