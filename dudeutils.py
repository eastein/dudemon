import itertools
import datediff

"""
jim is here now
jim and rhys will be here in 23 minutes.
nobody is here now
"""
def whom(state, now, when) :
	whom = list()
	for who in state :
		if 'e' not in state[who] or 's' not in state[who] :
			continue

		if when <= state[who]['e'] and state[who]['s'] <= when :
			whom.append(who)
	whom.sort()
	plural = len(whom) > 1

	if len(whom) > 2 :
		whom = ', '.join(whom[:-1]) + ', and ' + whom[-1]
	elif len(whom) == 2 :
		whom = '%s and %s' % (whom[0], whom[1])
	elif len(whom) == 0 :
		whom = 'nobody'
	else :
		whom = whom[0]

	if now == when :
		temporal = 'now'
		if plural :
			verbal = 'are'
		else :
			verbal = 'is'
	else :
		temporal = 'in %s' % datediff.differ(when - now)
		verbal = 'will be'

	return '%s %s here %s.' % (whom, verbal, temporal)


def when(state, now, forward=True, count=1) :
	ARRIVE = 0
	LEAVE = 1
	FUTURE = 0
	PAST = 1
	sort_pairs = [
		(ARRIVE, 's'),
		(LEAVE, 'e')
	]
	def find_events(forward=forward) :
		filt = {
			True : lambda ts: ts >= now,
			False : lambda ts: ts < now
		}[forward]
		events_tsdict = dict()

		for person,st in state.items() :
			# extract relevant data from all states
			for etype,k in sort_pairs :
				ets = st[k]
				if not filt(ets) :
					continue

				# add granularity? it'd be nice to group people into smaller buckets if
				# they arrive close together in time
				events_tsdict.setdefault(ets, list())
				events_tsdict[ets].append((person, etype))

		return events_tsdict

	ev = find_events()
	phrases = {
		FUTURE : {
			ARRIVE : '%s will be here in %s',
			LEAVE : '%s will leave in %s'
		},
		PAST : {
			ARRIVE : '%s got here %s ago',
			LEAVE : '%s left %s ago'
		}
	}
	tskeys = ev.keys()
	tskeys.sort()
	if not ev :
		forward = not forward
		ev = find_events(forward=forward)
		tskeys = ev.keys()
		tskeys.sort(reverse=True)

	tense = {
		True : FUTURE,
		False: PAST
	}[forward]

	def emit_events_english(tskeys, ev) :
		for ts in tskeys :
			for e in ev[ts] :
				if count <= 0 :
					raise StopIteration
				person, event = e
				yield phrases[tense][event] % (person, datediff.differ(abs(ts - now)))

	if not tskeys :
		return 'The only thing I know is that I know nothing.'

	return oxford(itertools.islice(emit_events_english(tskeys, ev), 0, count)) + '.'

def overlap(state, s, e) :
	whom = list()
	for who in state :
		if 'e' not in state[who] or 's' not in state[who] :
			continue

		w_s = state[who]['s']
		w_e = state[who]['e']

		if s < w_s and e > w_e :
			whom.append(who)
			continue
		elif s >= w_s and s <= w_e :
			whom.append(who)
			continue
		elif e >= w_s and e <= w_e :
			whom.append(who)
			continue

	whom.sort()
	return whom

def oxford(l) :
	l = list(l)
	if not l :
		raise RuntimeError
	if len(l) > 2 :
		l[len(l)-1] = 'and %s' % l[len(l)-1]
		return ', '.join(l)
	elif len(l) == 2 :
		return '%s and %s' % (l[0], l[1])
	else :
		return l[0]
