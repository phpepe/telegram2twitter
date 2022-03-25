from pprint import pprint
import textwrap

MAXCHARS = 280

def split(text, charlen, separator):
    '''
    @TODO https://www.reddit.com/r/learnpython/comments/2fv6z2/help_splitting_strings_to_make_tweets_out_of_text/
    @TODO https://github.com/kossnocorp/chirrapp/blob/master/src/app/_lib/split/index.js
    :param text:
    :param charlen:
    :param separator:
    :return:
    '''
    result = []
    # split by line end
    pharagraphs =  text.split("\n")

    lines = [p.strip() for p in pharagraphs]
    lines = [p for p in lines if p is not '']

    for i in lines:
        if len(i) >= charlen:
            result += textwrap.wrap(i.strip(), charlen, break_long_words=False, fix_sentence_endings=True)
        else:
            result.append(i)

    # Join pharagrafs too small

    for k, t in enumerate(result):
        rlen = len(result)
        len1 = len(t)
        if k + 1 < rlen:
            # if not last
            t2 = result[k + 1]
            len2 = len(result[k + 1])
            if len1 + len2 <= charlen:
                # if join is small
                j = t + "\n" + t2
                result[k] = j
                del result[k + 1]

    # add separator
    rlen = len(result)
    for i, t in enumerate(result):
        if i < rlen - 1:
            result[i] += separator

    return result


def simulate(peaces):
    for i in peaces:
        print('^^^^' + str(len(i)) + '^^^^')
        print(i)

