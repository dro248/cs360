CXX=		g++ $(CCFLAGS) $(LIBS)
threads=	threads.o
OBJS =		$(threads)

LIBS=		-pthread -std=c++11

CCFLAGS= -g

all:		threads

threads:	$(threads)
		$(CXX) -o threads $(threads) $(LIBS)

clean:
		rm -f $(OBJS) $(OBJS:.o=.d)

realclean:
		rm -f $(OBJS) $(OBJS:.o=.d) threads

%.o : %.cc
		$(CXX) -c -o $@ -MD -MP ${CPPFLAGS} ${CXXFLAGS} $<

-include	$(OBJS:.o=.d)
