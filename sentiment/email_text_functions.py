import email_text_processing as etp
import sys

utils = etp.UtilMethods()

def get_tagged_out(text,senttag,sentscore,rejtag,rejscore):
    ''' '''
    assert type(text) == str
    tagger = etp.Tagger()
    splitter = etp.Splitter()

    splitted_sentences = splitter.split(text)
    tagged_sentences = tagger.basic_tag(splitted_sentences)

    dicttagger = etp.DictionaryTagger(utils.gen_pol_dict_frm_twofiles('data_files/positive_words.csv','data_files/negative_words.csv',','))
    # print('default tagging')
    dict_tagged_sentences = dicttagger.tag(tagged_sentences,utils.default_evaluator,senttag,sentscore)
    # utils.print_tagsent(dict_tagged_sentences)
    # print('tagging by stemming')
    # dict_tagged_sentences = dicttagger.tag(dict_tagged_sentences,utils.default_evaluator,senttag,sentscore,preprocess_function=utils.prepro_stemming,process_on='stem_string')
    # utils.print_tagsent(dict_tagged_sentences)
    # print('tagging by stopword removing')
    # dict_tagged_sentences = dicttagger.tag(dict_tagged_sentences,utils.default_evaluator,senttag,sentscore,preprocess_function=utils.prepro_stopword_removal)
    # utils.print_tagsent(dict_tagged_sentences)

    rejtagger = etp.DictionaryTagger(utils.gen_rej_dict())
    # rej_tagged_sentences = rejtagger.tag(pos_tagged_sentences,basic_analysis.evaluator_rej,'rejtag','rejscore')
    # print('reject tagger')
    rej_dict_tagged_sentences = rejtagger.tag(dict_tagged_sentences,utils.evaluator_rej,rejtag,rejscore)
    return rej_dict_tagged_sentences

def get_processed_text(text):
    ''' out processed text'''
    assert type(text) == str
    text = text.lower()
    tagger = etp.Tagger()
    splitter = etp.Splitter()

    splitted_sentences = splitter.split(text)
    tagged_sentences = tagger.basic_tag(splitted_sentences)
    return tagged_sentences

def get_regex_rejection(mail_text):
    ''' '''
    assert type(mail_text) == str
    mail_text = mail_text.lower()
    processed_text = get_processed_text(mail_text)
    remove = etp.RegexMatching().match_sent_taggedsent_rejection(processed_text) or \
             etp.RegexMatching().match_sent_text_rejection(mail_text)
    return remove

def test_code(text=None):
    if text is None:
        text = """What can I say about this place. The staff of the restaurant is nice and the eggplant is not bad. \
        Apart from that, very uninspired food, lack of atmosphere and too expensive. I am a staunch vegetarian and was \
        sorely dissapointed with the veggie options on the menu. Will be the last time I visit, I recommend others to avoid."""
    tagged_text = get_tagged_out(text,'sent_tag','sent_score','rej_tag','rej_score')
    print(tagged_text)
    # utils.print_tagsent(tagged_text)
    reject_decision = 'Reject' if utils.analyze_dict_rej(tagged_text,'rej_tag')==1 else 'Not Reject'
    print(text)
    print('reject dict matching',reject_decision)
    decision_regex = 'Reject' if etp.RegexMatching().match_sent_text_rejection(text)==1 else 'Not Reject'
    print('reject regex matching',decision_regex)
    decision_tag_reg = 'Reject' if etp.RegexMatching().match_sent_taggedsent_rejection(tagged_text)==1 else 'Not Reject'
    print('reject regex on tagged sent',decision_tag_reg)

if __name__ == '__main__':
    if len(sys.argv)>1:
        text=sys.argv[1]
        test_code(text)
    else:
        test_code()

