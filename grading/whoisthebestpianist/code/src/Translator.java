import java.io.*;
import java.util.*;
import java.util.regex.*;

import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;

public class Translator {
	public static final String file_train = "data/train.txt";
	public static final String file_test = "data/test.txt";
	public static final String file_dict = "data/dict.txt";
	public static final String file_dict_verb = "data/dict_verb_morphology.txt";
	public static final String file_bigram = "data/nyt_200811.txt";  //corpus for traning language model
	public static final String file_chinese_pos_model = "stanford-postagger-full/models/chinese-distsim.tagger";

	private static HashMap<String, ArrayList<String>> dict_verb; //e.g. begin: beginning, begins, began, begun
	private static HashMap<String, ArrayList<String>> dict;
	private static MaxentTagger maxentTagger;
	private static HolbrookCorpus bigram_corpus;
    private static LaplaceBigramLanguageModel bigram_model;

	public Translator() {
        dict = new HashMap<String, ArrayList<String>>();		
	    loadDictionary(file_dict);
	    dict_verb = new HashMap<String, ArrayList<String>>();
	    loadVerbMorphologyDictionary(file_dict_verb);

	    maxentTagger = new MaxentTagger(file_chinese_pos_model); //initialize the tagger

	    bigram_corpus = new HolbrookCorpus(file_bigram);
        bigram_model = new LaplaceBigramLanguageModel(bigram_corpus);
	}
    
	private void loadVerbMorphologyDictionary (String file_dict_verb) {
		try {
	    	BufferedReader br = new BufferedReader(new FileReader(file_dict_verb));
	        String line;
	        while ((line = br.readLine()) != null) {
	        	if (line.trim().equals("")) continue;
	            String[] tmp = line.split("::");
	            String key = tmp[0].trim();
	            String[] vals = tmp[1].trim().split("\\s*,,\\s*");
	            assert vals.length == 4;
	            ArrayList<String> vals_list = new ArrayList<String>(Arrays.asList(vals));
	            dict_verb.put(key, vals_list);
	        }
	        br.close();
	    } catch (IOException e) {
	        e.printStackTrace(System.out);
		}
	}

	private void loadDictionary(String file_dict) {
		try {
	    	BufferedReader br = new BufferedReader(new FileReader(file_dict));
	        String line;
	        while ((line = br.readLine()) != null) {
	        	if (line.trim().equals("")) continue;
	            String[] tmp = line.split("::");
	            String key = tmp[0].trim();
	            String[] vals = tmp[1].trim().split("\\s*,,\\s*");
	            ArrayList<String> vals_list = new ArrayList<String>(Arrays.asList(vals));
	            if (dict.containsKey(key))
	            	vals_list.addAll(dict.get(key));
	            //Eliminate duplicates using Hashset
	            HashSet<String> s = new HashSet<String>();
				s.addAll(vals_list);
				vals_list.clear();
				vals_list.addAll(s);
	            dict.put(key, vals_list);
	        }
	        br.close();
	    } catch (IOException e) {
	        e.printStackTrace(System.out);
		}
	}

	public void translateFile (String file_name, boolean consolePrint){
		try {
	    	BufferedReader br = new BufferedReader(new FileReader(file_name));
			PrintWriter pw = new PrintWriter (file_name.substring(0, file_name.lastIndexOf(".txt")) + "_translated.txt");
	        String line;
	        while ((line = br.readLine()) != null) {
	        	if (line.trim().equals("")) continue;
	        	String translation = translateSentence(line);
	            pw.println(translation);
	            if (consolePrint)
	            	System.out.println(translation + "\n---");
	        }
	        br.close();
	        pw.close();
	    } catch (IOException e) {
	        e.printStackTrace(System.out);
		}		
	}

	//The delimiter is #
	private String getTag(String word) {
		assert word != null;
		int index = word.lastIndexOf('#');
		assert index != -1 && index != word.length()-1;
		return word.substring(index+1);
	}

	private String getWord(String word) {
		assert word != null;
		int index = word.lastIndexOf('#');
		assert index != -1 && index != word.length()-1;
		return word.substring(0,index);
	} 

	//List contains a list of retrieved definitions (with tag if more than one definition)
	//tag is the tag of the chinese word
	private String pickWordFromDictionary(ArrayList<String> list, String tag) {
		assert list.size() >= 1;
		if (list.size() == 1) return list.get(0);

		//Best case: perfect match, then just return the first found
		//No need to randomize as it's already done when loading the dictionary (we used a Hashmap...)
		for (String word : list) 
			if (getTag(word).equals(tag))
				return getWord(word);

		//We then do not differentiate verbs (start with V), nouns (start with N), 
		//                            adjectives (VA and JJ), conjuctions (CC, CS)
		for (String word : list) {
			String t = getTag(word);
			if (   (t.charAt(0) == 'V' && tag.charAt(0) == 'V')
				|| (t.charAt(0) == 'N' && tag.charAt(0) == 'N')
				|| (t.equals("VA") && tag.equals("JJ"))
				|| (t.equals("JJ") && tag.equals("VA"))
				|| (t.equals("CS") && tag.equals("CC"))
				|| (t.equals("CC") && tag.equals("CS"))		)
				return getWord(word);
		}

		//Well, last resort, return a random word...
		return getWord(list.get(0));
	}

	private String directTranslate(String sentenceC, boolean keepTag) {
		String sentenceE = "";
		String[] arr = sentenceC.split("\\s");
		for (String str : arr) {
			String word = str.substring(0,str.indexOf('#')).trim(); //get the word before POS tag
			/* Note that the word may have number attached to it; e.g. 1958年, so dump it to result first */
			int i = 0;
			for (i = 0; i < word.length(); i++) {
				if (!Character.isDigit(word.charAt(i)))
					break;
				else
					sentenceE += word.charAt(i);
			}
			word = word.substring(i);
			if (!word.equals("") && !dict.containsKey(word))
				System.out.println("!!!!!!!!!!!! THE WORD IS NOT IN THE DICTIONARY !!!!!!!!!!!!!! VERY BAD!!!!!!!!");
			else if (!word.equals("")) {
				//Need heuristics to select the word, not just the first word
				//NOTE that VA and JJ are very similar ~~~
				sentenceE += pickWordFromDictionary(dict.get(word), str.substring(str.indexOf('#')+1));
			}
			if (keepTag)
				sentenceE +=  str.substring(str.indexOf('#'));
			sentenceE += " ";
		}
        return sentenceE;
	}

	private String fixPunctuationSpace(String s) {
 		s = s.replaceAll("\\s{2,}", " ");
 		Matcher m = Pattern.compile("\\s([.,?!\'\":;])").matcher(s);
 		while (m.find()){
 			s = m.replaceFirst("$1");
 			m.reset(s);
 		}
 		return s;
	}

	private String fixCapitalization(String s) {
 		s = "" + Character.toUpperCase(s.charAt(0)) + s.substring(1);
 		Matcher m = Pattern.compile("([.?!]\\s)([a-z])").matcher(s);
 		while (m.find()){
 			char ch = m.group(2).charAt(0);
 			s = m.replaceFirst("$1" + Character.toUpperCase(ch));
 			m.reset(s);
 		}
 		return s;
	}

	private String fixNumberSpace(String s) {
 		Matcher m = Pattern.compile("(\\d)([A-Za-z])").matcher(s);
 		while (m.find()){
 			s = m.replaceFirst("$1 $2");
 			m.reset(s);
 		}
 		return s;
	}

    private String fixDate(String s) {
        // "2 month" => "February"
        Matcher m = Pattern.compile("(\\d+)\\s(month)", Pattern.CASE_INSENSITIVE).matcher(s);
        while (m.find()){
            if (m.group(1).equals("1")) {
                s = m.replaceFirst("January");
            }
            if (m.group(1).equals("2")) {
                s = m.replaceFirst("February");
            }
            if (m.group(1).equals("3")) {
                s = m.replaceFirst("March");
            }
            if (m.group(1).equals("4")) {
                s = m.replaceFirst("April");
            }
            if (m.group(1).equals("5")) {
                s = m.replaceFirst("May");
            }
            if (m.group(1).equals("6")) {
                s = m.replaceFirst("June");
            }
            if (m.group(1).equals("7")) {
                s = m.replaceFirst("July");
            }
            if (m.group(1).equals("8")) {
                s = m.replaceFirst("August");
            }
            if (m.group(1).equals("9")) {
                s = m.replaceFirst("September");
            }
            if (m.group(1).equals("10")) {
                s = m.replaceFirst("October");
            }
            if (m.group(1).equals("11")) {
                s = m.replaceFirst("November");
            }
            if (m.group(1).equals("12")) {
                s = m.replaceFirst("December");
            }
            m.reset(s);
        }

        // "February 15 day" => "On February 15th"
        final String months = "(January|February|March|April|May|June|July|August|September|October|November|December)";
        m = Pattern.compile(months+"\\s(\\d+)\\s(day|sun)", Pattern.CASE_INSENSITIVE).matcher(s);
        while (m.find()){
            s = m.replaceFirst("on $1 $2th");
            m.reset(s);
        }
        
        // "1983 year" => "in 1983"
        m = Pattern.compile("(\\d{4})(\\s)(year)", Pattern.CASE_INSENSITIVE).matcher(s);
        while (m.find()){
            s = m.replaceFirst("in $1");
            m.reset(s);
        }

        // make sure the first letter is uppercase
        s = s.substring(0,1).toUpperCase() + s.substring(1,s.length());

        return s;
    }

    private String fixAge(String s) {
        Matcher m = Pattern.compile("(\\d+)(\\s)(age|year)", Pattern.CASE_INSENSITIVE).matcher(s);
        while (m.find()){
            s = m.replaceFirst("at age $1");
            m.reset(s);
        }
        return s;
    }

    /* Pua a whitespace in between segments */
    public String segmentChinese (String str) {
    	String output = "";
		int begin_idx = 0;
		while (begin_idx < str.length()) {
			int end_idx = begin_idx;
            // match as far as possible
			for (int idx = begin_idx + 1; idx <= str.length(); idx++)
				if (dict.containsKey(str.substring(begin_idx,idx)))
					end_idx = idx;

            if (begin_idx == end_idx) {//must be punctuation
            	output += str.substring(begin_idx, begin_idx + 1);
            	begin_idx++;
            } else {
            	output += str.substring(begin_idx,end_idx) + " ";
            	begin_idx = end_idx;
            }
        }
        return output;
    }

    public String posTagChinese (String str) {
    	String output = maxentTagger.tagString(str);
    	//System.out.println(output);
    	return output;
	}

    private double calculateScore(String[] words) {
        double score = 0.0;
        for (int i = 0; i < words.length-1; i++) {
            String[] border_bits = new String[2];
            
            String[] word_bits1 = words[i].split("\\s+");
            if (word_bits1.length == 0) continue;
            border_bits[0] = word_bits1[word_bits1.length-1];

            String[] word_bits2 = words[i+1].split("\\s+");
            if (word_bits2.length == 0) continue;
            border_bits[1] = word_bits2[word_bits2.length-1];

            score += bigram_model.score(Arrays.asList(border_bits));
        }
        return score;
    }

    void permutateWords(String[] words, int cursor, double[] best_score, String[] best_words) {
        if (cursor >= words.length-2) {// don't permutate last word
            double score = calculateScore(words);
            //System.out.println("score: " + score + "best score: " + best_score[0]);
            if (score > best_score[0]) {
                best_score[0] = score;
                for (int i = 0; i < words.length; i++) {
                    best_words[i] = words[i];
                }
                //System.out.println("best words: " + Arrays.toString(best_words) + "best score: " + best_score[0]);
            }
        } else {
            permutateWords(words, cursor+1, best_score, best_words);
            for (int i = cursor+1; i < words.length; i++) {
                String word_cursor = words[cursor];
                words[cursor] = words[i];
                words[i] = word_cursor;
                permutateWords(words, cursor+1, best_score, best_words);
            }
        }
    }
    
    private String fixOrderByBigramForClause(String clause) {
        if (clause.trim().equals("")) return "";
        
        // one word is one entry in dictionary, which might be a phrase
        String[] words = clause.split("#\\w+");
        // remove "" entries in words
        Vector<String> v = new Vector<String>();
        for (int i = 0; i < words.length; i++) {
            if (!words[i].matches("\\s*")) {
                v.add(words[i]);
            }
        }
        words = v.toArray(new String[v.size()]);
        int block_size = 5;
        if (words.length < block_size) {
            block_size = words.length;
        }

        for (int i = 0; i <= words.length-block_size; i++) {
            double[] best_score = new double[1];
            best_score[0] = -1/0.0;
            String[] words_in_block = Arrays.copyOfRange(words,i,i+block_size);
            String[] best_words_in_block = words_in_block.clone();

            //System.out.println("trying to rearrange by bigram:" + Arrays.toString(words_in_block));
            if (words_in_block.length <= 2) continue;
            // don't permutate the first word
            permutateWords(words_in_block,1,best_score,best_words_in_block);

            //System.out.println("done, the best is: " + Arrays.toString(best_words_in_block));

            for (int j = 0; j < block_size; j++) {
                words[i+j] = best_words_in_block[j];
            }
        }
        
        String most_likely_clause = "";
        for (int i=0; i<words.length-1; i++) {
            most_likely_clause += words[i];
            most_likely_clause += " ";
        }
        
        most_likely_clause += words[words.length-1];
        if (!clause.equals(most_likely_clause)) {
            System.out.println("fixed 1 clause:\n" + clause + "=>\n" + most_likely_clause);
        }
        return most_likely_clause;
    }

    private String fixOrderByBigram(String s) {
        String s_new = "";
        String[] clauses = s.split("[,.]");
        for (int i=0; i<clauses.length-2; i++) {
            s_new += fixOrderByBigramForClause(clauses[i]);
            s_new += ", ";
        }
        //the last one is a white space
        s_new += fixOrderByBigramForClause(clauses[clauses.length-2]);
        s_new += ".";
        return s_new;
    }

    /*********************
     *      Rules        *
     *********************
     *** Note: all verbs/verb phrases in the dictionary are in their original form
	 * 
     * Future Simple (FS):
     * -------------------
     * If got 将, 即将, 将要, 将会, then forward search for verbs and change verbs to "will do"
     *
     * Present Progressive (PPR): 
     * -------------------------
     * If got 正在, 正, then forward search for verbs and change verbs to "be doing"
     * If got 着#AS
     *
     * Present Perfect (PPE):
     * ----------------------
     * If got 已经, 已, then forward search for verbs and change to "have done"
     * 
	 * Pressent Perfect Progressive (PPP):
	 * -----------------------------------
	 * Time signal: 近年来, 这段时..., 这些天、日、月、年、星期、周; change verbs to "have been doing"
	 *
     * Past Simple (PS):
     * -----------------
     * 1. Time signal (tagged with #NT): 上个, 当日, 当晚, 当年, 去年, 昨, specific time (2月18号, in 1999)  
     * 2. Action signal: 了#AS (e.g. 举行了一场演出)
     * 3. Speicific verb: 说, 想, 觉得, 看见, 听到, 认为, 感觉, 感到 
	 *
	 * Simple Present Tense (SPT):
	 * ---------------------------
	 * If all the other failed...
	 *
	 * Fix 3rd person:
	 * ---------------
	 * 1. have -> has
	 * 2. verb -> 3rd person verb
	 *
	 * Fix "be": am, are, be, been, being, is, was, were:
	 * --------------------------------------------------
	 * Decide on the tense first
	 * 1. Present: am, are, is
	 * 2. Progressive: being
	 * 3. Perfect: been
	 * 4. Past: was, were
	 * 5. Future: [will] be
	 *
	 ****************************************************************
	 * Procedures: 
	 *
	 * 1. Split up the sentence by , ; : 、first (don't consider . or ? as they mark the end of sentence)
     * 2. Assign each subsentence a tense (look around the neighbors if cannot decide)
     * 3. correct the tense of each subsentence using the dictionary
     */
    /** Grammatical Person */
    public enum GPerson{FIRST, SECOND, THIRD};

    /**
     * @param: s_tagged is the English subsentence with tags
     * @param: c_tagged is the Chinese subsentence with tags
     */
    private String findTense(String s_tagged, String c_tagged) {
    	//Get the tag free version for Chinese sentence
    	String c = c_tagged.replaceAll("#[A-Z]+","");
    	Matcher m = null;

    	if (has(c,"即将") || has(c,"将要") || has(c,"将会") || has(c_tagged," 将#"))
    		return "FS";

    	if (has(c,"正在") || has(c_tagged," 正#") || has(c_tagged," 着#AS"))
    		return "PPR";

    	if (has(c,"已经") || has(c_tagged," 已#"))
    		return "PPE";

    	m = Pattern.compile("(近年来)|(这[段些](日|天|月|年|周|星期))").matcher(c);
 		if(m.find())
 			return "PPP";

 		/* 1. Time signal (tagged with #NT): 上个, 当日, 当晚, 当年, 去年, 昨, specific time (2月18号, in 1999)  
     	 * 2. Action signal: 了#AS (e.g. 举行了一场演出)
     	 * 3. Speicific verb: 说, 想, 觉得, 看见, 听到, 认为, 感觉, 感到 
     	 */
 		m = Pattern.compile("(说|想|觉得|看见|听见|听到|认为|感觉|感到)" + "|"
 							+ "(\\s了#AS)" + "|"
 							+ "((当|昨|去|上个).{1,2}#NT)"   + "|"
 							+ "(\\d+[年月日号岁])" + "|"
 							+ "((星期|周)[一二三四五六日天])").matcher(c_tagged);
 		if (m.find())
 			return "PS";
    	return "";
    } 

    /* Utility funciton for checking whether s contains subString */
    public static boolean has (String s, String subString) {
    	if (s == null || subString == null)
    		return false;
    	return s.indexOf(subString) != -1;
    } 

    private String fixVerbMorphology(String s_tagged, String sentenceC_tagged) {
    	String c_tagged = sentenceC_tagged; //avoid long variable name
    	String c = c_tagged.replaceAll("#[A-Z]+",""); //strip tags for Chinese
    	String[] sc = c_tagged.split("\\s*[，；：、]#PU\\s*");  //subsentences - Chinese
    	String[] ss = s_tagged.split("\\s*[,;:]#PU\\s*");    //subsentences - English
    	assert sc.length == ss. length;
    	int len = sc.length;

    	//Get the punctuation delimiters
       	ArrayList<String> puncs = new ArrayList<String>();
     	Matcher m = Pattern.compile("([,;:])#PU").matcher(s_tagged);
 		while(m.find())
 			puncs.add(m.group(1));
 		assert ss.length == puncs.size() + 1;

    	/*=============================== Determine Tense ========================*/
    	//Find tense for each subsentence
    	String[] tenses = new String[sc.length];
    	for (int i = 0; i < len; i++)
    		tenses[i] = findTense(ss[i], sc[i]);

    	//If all tenses are missing, assign SPT for all
    	String tmp = "";
    	for (String tense : tenses)	tmp += tense;
    	if (tmp.trim().equals(""))
    		for (int i = 0; i < len; i++)
    			tenses[i] = "SPT";

    	//Otherwise, search the tense of the 
    	//        EITHER nearest-neighbor (follow the proceeding tense to break tie)
    	//        OR     following its proceeding tense
		ArrayList<Integer> nonEmptyTenseIndex = new ArrayList<Integer>();
		for (int i = 0; i < len; i++)
			if (!tenses[i].equals("")) 
				nonEmptyTenseIndex.add(i);
		int[] sepIndex = new int[nonEmptyTenseIndex.size()];
		for (int i = 0; i < sepIndex.length; i++){
			if (i == sepIndex.length-1){
				sepIndex[i] = len-1;
			}else{
				/* EITHER: nearest-neighbor approach */
				//sepIndex[i] = (nonEmptyTenseIndex.get(i) + nonEmptyTenseIndex.get(i+1)) / 2; //i.e. taking floor
				/* OR: following is proceeding tense */
				sepIndex[i] = nonEmptyTenseIndex.get(i+1) - 1;
			}
		}
		for (int i = 0; i < len; i++){
			for (int j = 0; j < sepIndex.length; j++){
				if ((j ==0 && i <= sepIndex[j]) || (j > 0 && i <= sepIndex[j] && i > sepIndex[j-1])){
					tenses[i] = tenses[nonEmptyTenseIndex.get(j)];
					break;
				}
			}
		}
		/* Debugging code */
		// System.out.println(c);
		// for (int i = 0; i < tenses.length; i++){
		// 	if (i < tenses.length-1)
		// 		System.out.print(tenses[i] + ", ");
		// 	else
		// 		System.out.println(tenses[i]);
		// }

    	/*============================= Correct Verbs  ========================*/
    	for (int i = 0; i < len; i++)
    		ss[i] = correctVerb(ss[i], sc[i], tenses[i]);

    	String s = "";
    	for (int i = 0; i < len; i++){
			s += ss[i].trim();
			if (i != len-1)
				s += puncs.get(i) + " ";
		}

    	return s;
    }

    /** 
     * @return returned String has no tags!!! 
     */
    private String correctVerb(String s_tagged, String c_tagged, String tense){

    	String s = s_tagged.replaceAll("#[A-Z]+",""); //strip off all tags
    	ArrayList<String> s_arr = new ArrayList<String>(Arrays.asList(s.split("\\s+")));
    	int len = s_arr.size();

    	//First correct idiomatic grammar usage: e.g. begin/start/finish/with/by/go doing, 
    	for (int i = 0; i < len-1; i++){
    		String word = s_arr.get(i);
    		String nword = s_arr.get(i+1);
    		if (!dict_verb.containsKey(nword)) continue;
    		if (word.matches("begin|start|finish|with|by|go"))
    			s_arr.set(i+1, dict_verb.get(nword).get(0));
    	}

    	//Pick out all the verbs (i.e. it's be or they appear in verb morphology dictionary)
    	ArrayList<String> verbs = new ArrayList<String>();
    	ArrayList<Integer> verbIndices = new ArrayList<Integer>();
    	for (int i = 0; i < len; i++){
    		if (dict_verb.containsKey(s_arr.get(i))) {
    			verbs.add(s_arr.get(i));
    			verbIndices.add(i);
    		}
    	}
    	int vlen = verbs.size();
    	//no verbs at all!
    	if (vlen == 0)
    		return s;

    	if (tense.equals("FS")){
    		if (s_arr.contains("will")) //if "will" is present, get rid of it first
    			s_arr.set(s_arr.indexOf("will"), "");
    		//change the first verb to "will do"
    		String verb = verbs.get(0);
    		s_arr.set(verbIndices.get(0), "will " + verb);
    	}else if (tense.equals("PPR")){
    		for (int i = 0; i < vlen; i++){
    			String verb_ppr = dict_verb.get(verbs.get(i)).get(0);//doing form
    			int verbInd = verbIndices.get(i);
    			s_arr.set(verbInd, "be " + verb_ppr);
    		}
    	}else if(tense.equals("PPE")){
    		if (s_arr.contains("already")) //if "already" is present, get rif of it
    			s_arr.set(s_arr.indexOf("already"), "");
    		for (int i = 0; i < vlen; i++){
    			String verb_ppe = dict_verb.get(verbs.get(i)).get(3);//done form
    			int verbInd = verbIndices.get(i);
    			s_arr.set(verbInd, "have already " + verb_ppe);
    		}
    	}else if (tense.equals("PPP")){
    		for (int i = 0; i < vlen; i++){
    			String verb_ppr = dict_verb.get(verbs.get(i)).get(0);//doing form
    			int verbInd = verbIndices.get(i);
    			s_arr.set(verbInd, "have been " + verb_ppr);
    		}
    	}else if (tense.equals("PS")){
    		for (int i = 0; i < vlen; i++){
    			String verb_ps = dict_verb.get(verbs.get(i)).get(2);
    			int verbInd = verbIndices.get(i);
    			s_arr.set(verbInd, verb_ps);
    		}
    	}

    	//Reconstruct the string array
		s = "";
		for (int i = 0; i < len; i++){
			s += s_arr.get(i).trim();
			if (i != len-1)
				s += " ";
		}
		s = s.replace(" be be ", " be "); 		//avoid double be
		s = s.replace(" not be ", " be not ");  //handle negation on be-verb
		s_arr = new ArrayList<String>(Arrays.asList(s.split("\\s+")));
		len = s_arr.size();

    	//Sweep for be, have, and determine correct form for grammatical person
    	//First, determine Grammatical Person (GPerson)
    	GPerson gp = GPerson.THIRD;
    	if (has(c_tagged, "我"))
    		gp = GPerson.FIRST;
    	else if (has(c_tagged, "你"))
    		gp = GPerson.SECOND;

    	for (int i = 0; i < len; i++){
    		String word = s_arr.get(i);
    		if (!dict_verb.containsKey(word)) continue;
    		
    		if (tense.equals("FS")){
    			continue;
    		}else if (tense.equals("PPR") && word.equals("be")){
    			switch (gp){
    				case FIRST: s_arr.set(i, "am"); break;
    				case SECOND: s_arr.set(i, "are"); break;
    				case THIRD: s_arr.set(i, "is"); break;
    			}
    		}else if ((tense.equals("PPE") || tense.equals("PPP")) && word.equals("have")){
    			switch (gp){
    				case THIRD: s_arr.set(i, "has"); break;
    			}
    		}else if (tense.equals("PS") && word.equals("be")){
    			switch(gp){
    				case THIRD: case FIRST: s_arr.set(i, "was");break;
    				case SECOND: s_arr.set(i,"were");break;
    			}
    		}else if (tense.equals("SPT")){
    			if(word.equals("be")){
    				switch (gp){
    					case FIRST: s_arr.set(i, "am"); break;
    					case SECOND: s_arr.set(i, "are"); break;
    					case THIRD: s_arr.set(i, "is"); break;
    				}
    			}else{
    				switch(gp){
    					case THIRD: s_arr.set(i, dict_verb.get(word).get(1)); break;
    				}
    			}
    		}
    	}

    	s = "";
		for (int i = 0; i < len; i++){
			s += s_arr.get(i).trim();
			if (i != len-1)
				s += " ";
		}
    	return s;
    }


	public String translateSentence (String sentenceC) {
		String s = "";
		String sentenceC_segmented = segmentChinese(sentenceC);
		String sentenceC_tagged = posTagChinese(sentenceC_segmented );
		s = directTranslate(sentenceC_tagged, true); //true to keep the tags!
		s = fixVerbMorphology(s, sentenceC_tagged);  //note that s must have tags!
		s = s.replace("()", "");   //() is a place holder in dictionary for omitted translation
		s = fixPunctuationSpace(s);
		s = fixCapitalization(s);
		s = fixNumberSpace(s);
        s = fixDate(s);
        s = fixAge(s);
        //s = fixOrderByBigram(s);
		return s;
    }

    //Utility Helper
	public static void printDictionary(HashMap<String, ArrayList<String>> dict) {
		for (String key : dict.keySet()) {
			System.out.print(key + ": ");
			ArrayList<String> vals = dict.get(key);
			for (int i = 0; i < vals.size(); i++){
				if (i < vals.size() - 1)
					System.out.print(vals.get(i) + ", ");
				else
					System.out.println(vals.get(i));
			}
		}
	}

	//Utility Helper
	public static void printByteArray(byte[] arr) {
		for (int i = 0; i < arr.length; i++){
			if (i < arr.length - 1)
				System.out.print(arr[i] + ", ");
			else
				System.out.println(arr[i]);
		}
	}

	public static void main(String[] args) {
        System.out.println(   "\n==================================== IMPORTANT =====================================\n"
                            + "This program requires a Java 1.7.0_51 JDK.\n"
                            + "Not running in this environment may leads to error when handling Chinese characters.\n"
                            + "Also note that all text files are encoded with UTF-8 encoding.\n"
                            + "====================================================================================\n");
        Translator model = new Translator();
        //should be file_train, or file_test
        //use "true" to turn on Console Print of the translated text
        model.translateFile(file_test, true);
  	}
}
