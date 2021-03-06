import itertools
import datediff

"""
jim is here now
jim and rhys will be here in 23 minutes.
nobody is here now

@param now integer unix timestamp asserting that that is when now should be considered to be
@param when integer unix timestamp indicating when the requestor wants to know about
@param nv a sync_logic.NetworkView object from pamela_probe, if set. Can be used to check the set of nodes on the
          network.
"""


def whom(state, now, when, nv=None):
    # determine present macs if possible to find & also relevant
    present_macs = None
    if (now == when) and (nv is not None) and nv.synced:
        present_macs = set([n[0] for n in nv.net])

    whomset = set()
    for who in state:
        period_set = ('e' in state[who] and 's' in state[who])
        mac_set = 'macs' in state[who]

        if period_set:
            if when <= state[who]['e'] and state[who]['s'] <= when:
                whomset.add(who)

        # if mac presence is relevant, and this person has a mac set... check it
        if mac_set and present_macs:
            ms = set(state[who]['macs'])
            if ms.intersection(present_macs):
                whomset.add(who)

    whom = list(whomset)
    whom.sort()
    plural = len(whom) > 1

    if len(whom) > 2:
        whom = ', '.join(whom[:-1]) + ', and ' + whom[-1]
    elif len(whom) == 2:
        whom = '%s and %s' % (whom[0], whom[1])
    elif len(whom) == 0:
        whom = 'nobody'
    else:
        whom = whom[0]

    if now == when:
        temporal = 'now'
        if plural:
            verbal = 'are'
        else:
            verbal = 'is'
    else:
        temporal = 'in %s' % datediff.differ(when - now)
        verbal = 'will be'

    return '%s %s here %s.' % (whom, verbal, temporal)


def when(state, now, count=1):
    ARRIVE = 0
    LEAVE = 1
    FUTURE = 0
    PAST = 1
    sort_pairs = [
        (ARRIVE, 's'),
        (LEAVE, 'e')
    ]

    def find_events():
        events_tsdict = dict()

        for person, st in state.items():
            if not st:
                continue

            # extract relevant data from all states
            for etype, k in sort_pairs:
                if k not in st:
                    continue

                ets = st[k]

                # add granularity? it'd be nice to group people into smaller buckets if
                # they arrive close together in time
                events_tsdict.setdefault(ets, list())
                events_tsdict[ets].append((person, etype))

        return events_tsdict

    ev = find_events()
    phrases = {
        FUTURE: {
            ARRIVE: '%s will be here in %s',
            LEAVE: '%s will leave in %s'
        },
        PAST: {
            ARRIVE: '%s got here %s ago',
            LEAVE: '%s left %s ago'
        }
    }

    def cmp_function(a, b):
        def value_function(v):
            return abs(v - now)

        return long.__cmp__(long(value_function(a)), long(value_function(b)))

    tskeys = ev.keys()
    tskeys.sort(cmp=cmp_function)

    def tense(ts):
        if ts >= now:
            return FUTURE
        else:
            return PAST

    def emit_events_english(tskeys, ev):
        already_mentioned = set()
        for ts in tskeys:
            for e in ev[ts]:
                person, event = e
                if person not in already_mentioned:
                    already_mentioned.add(person)
                    yield phrases[tense(ts)][event] % (person, datediff.differ(abs(ts - now)))

    if not tskeys:
        return 'The only thing I know is that I know nothing.'

    return oxford(itertools.islice(emit_events_english(tskeys, ev), 0, count)) + '.'


def overlap(state, s, e):
    whom = list()
    for who in state:
        if 'e' not in state[who] or 's' not in state[who]:
            continue

        w_s = state[who]['s']
        w_e = state[who]['e']

        if s < w_s and e > w_e:
            whom.append(who)
            continue
        elif s >= w_s and s <= w_e:
            whom.append(who)
            continue
        elif e >= w_s and e <= w_e:
            whom.append(who)
            continue

    whom.sort()
    return whom


def oxford(l):
    l = list(l)
    if not l:
        raise RuntimeError
    if len(l) > 2:
        l[len(l) - 1] = 'and %s' % l[len(l) - 1]
        return ', '.join(l)
    elif len(l) == 2:
        return '%s and %s' % (l[0], l[1])
    else:
        return l[0]
