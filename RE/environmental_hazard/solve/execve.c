#include <unistd.h>

int main(int argc, char* argv[]) {
  execve(argv[1], &argv[1], &argv[argc - 1]);
}
