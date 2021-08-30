#include <sys/time.h>

struct xtimer {
    struct timeval elapsed_time;
    struct timeval timestamp;
};

typedef struct xtimer   xtimer_t;

void timer_clear(xtimer_t *timer);
void timer_start(xtimer_t *timer);
void timer_stop(xtimer_t *timer);
double timer_elapsed_time(xtimer_t *timer);

