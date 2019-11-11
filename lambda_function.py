<html>

<head>
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-147552064-1"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
    
      gtag('config', 'UA-147552064-1');
    </script>

    <meta charset="utf-8">
    <meta content="width=device-width,initial-scale=1,minimal-ui" name="viewport">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="https://unpkg.com/vue-material@beta/dist/vue-material.min.css">
    <link rel="stylesheet" href="https://unpkg.com/vue-material@beta/dist/theme/default.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.32.0/codemirror.min.css" />
</head>

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-147552064-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'UA-147552064-1');
</script>

<body>
    <h1>pandas for everyone. 🐼</h1>
    <div id="app">
        
        <md-progress-bar md-mode="determinate" :md-value="amount"></md-progress-bar>
        <input type="range" v-model.number="amount"> {{ amount }}%
        
        <md-steppers>
            <md-step v-for="question in questions" :key=question.name md-done=question.status>
                <doctest-activity v-bind:layout-things=question.layoutItems
                    v-bind:question-name=question.name @updateprog="updateProgress" />
            </md-step>
        </md-steppers>
        
    </div>
    </div>
</body>
<script src="https://unpkg.com/vue"></script>
<script src="https://unpkg.com/vue-material@beta"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.32.0/codemirror.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/mode/python/python.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/vue-codemirror@4.0.6/dist/vue-codemirror.min.js"></script>

<script>
    Vue.use(VueMaterial.default)
    Vue.use(window.VueCodemirror)
    Vue.component('doctest-activity', {
        props: ['layoutThings', 'questionName'],
        data: function () {
            return {
                progress : 0,
                answer: "",
                layoutItems: this.layoutThings,
                title: this.questionName,
                num_try: 0,
                html_result:"",
                python_result:"",
                text_result:"",
                cmOptions: {
                    mode: 'python',
                    lineNumbers: true
                },
                cmReadOnly: {
                    lineNumbers: true,
                    mode: "python",
                    readOnly: true
                }
            }
        },
        methods: {
            postContents: function () {
                // only when submit question successfully
                this.num_try = this.num_try + 1;
                // comment: leaving the gatewayUrl empty - API will post back to itself
                const gatewayUrl = '';
                fetch(gatewayUrl, {
                    method: "POST",
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ shown: { 0: this.layoutItems[0].vModel }, editable: { 0: this.layoutItems[1].vModel }, qname:{0: this.questionName} })
                }).then(response => {
                    return response.json()
                }).then(data => {
                    this.answer = JSON.parse(JSON.stringify(data));
                    if(this.answer.isComplete == 1) {
                        this.num_try = 0;
                        this.html_result = this.answer.htmlFeedback;
                        this.python_result = this.answer.pythonFeedback;
                        this.text_result = "Congratulations!";
                    }
                    else if (this.num_try < 3){
                        this.html_result = this.answer.htmlFeedback;
                        this.python_result = this.answer.pythonFeedback;
                        this.text_result = "Sorry, try again";
                    }
                    else{
                        this.num_try = 0;
                        this.html_result = this.answer.htmlFeedback;
                        this.python_result = this.answer.pythonFeedback;
                        this.text_result = "You got it wrong again.\nScroll Below For the Correct Answer.\n\n\n\n\n\n\n\n\n\n\n\n" + this.answer.textFeedback;
                    }
                    this.progress = this.answer.progress * 10;
                    this.$emit('updateprog', this.progress)
                    return this.$emit('questionhandler', { data, questionName: this.questionName })
                })
            }
        },
        template:
        `
        <div>
        
        
        <h2 class="title-name">{{title}}</h2> 
            <div class="md-layout  md-gutter">
                <div id="cardGroupCreator" class="md-layout-item md-size-50">
                    
                    <md-table v-model="layoutItems[2].data" md-sort="name" md-sort-order="asc" md-card md-fixed-header>
                      <md-table-toolbar>
                            <h3>{{layoutItems[2].header}}</h3>
                      </md-table-toolbar>
                
                      <md-table-row slot="md-table-row" slot-scope="{ item }">
                        <md-table-cell md-label="ID" md-sort-by="id" md-numeric>{{ item.id }}</md-table-cell>
                        <md-table-cell md-label="NAME" md-sort-by="name">{{ item.name }}</md-table-cell>
                        <md-table-cell md-label="GENDER" md-sort-by="gender">{{ item.gender }}</md-table-cell>
                        <md-table-cell md-label="AGE" md-sort-by="age">{{ item.age }}</md-table-cell>
                        <md-table-cell md-label="CHILDREN" md-sort-by="children">{{ item.children }}</md-table-cell>
                        <md-table-cell md-label="RESIDENCE" md-sort-by="residence">{{ item.residence }}</md-table-cell>
                      </md-table-row>
                    </md-table>
                    
                    <md-card>
                    </md-card>
                    
                    <md-table v-model="layoutItems[3].data" md-sort="name" md-sort-order="asc" md-card md-fixed-header>
                      <md-table-toolbar>
                            <h3>{{layoutItems[3].header}}</h3>
                      </md-table-toolbar>
                
                      <md-table-row slot="md-table-row" slot-scope="{ item }">
                        <md-table-cell md-label="ID" md-sort-by="id" md-numeric>{{ item.id }}</md-table-cell>
                        <md-table-cell md-label="NAME" md-sort-by="name">{{ item.name }}</md-table-cell>
                        <md-table-cell md-label="GENDER" md-sort-by="gender">{{ item.gender }}</md-table-cell>
                        <md-table-cell md-label="AGE" md-sort-by="age">{{ item.age }}</md-table-cell>
                        <md-table-cell md-label="CHILDREN" md-sort-by="children">{{ item.children }}</md-table-cell>
                        <md-table-cell md-label="RESIDENCE" md-sort-by="residence">{{ item.residence }}</md-table-cell>
                      </md-table-row>
                    </md-table>
                    
                    
                </div>
                
                
                <div id="cardGroupPreview" class="md-layout-item md-size-50">
                    <md-card> <!-- Examples -->
                        <md-card-header>
                            <md-card-header-text>
                                <div class="md-title">{{layoutItems[0].header}}</div>
                                <div class="md-subhead">{{layoutItems[0].subHeader}}</div>
                                <div class="md-subhead">{{layoutItems[0].subHeader2}}</div>
                            </md-card-header-text>
                        </md-card-header>
                        <md-card-content>
                            <md-field>
                                 <codemirror class="editableTextarea" v-model="layoutItems[0].vModel" :options="cmReadOnly"></codemirror>
                            </md-field>
                        </md-card-content>
                    </md-card>
                    
                    <md-card>
                        <md-card-header>
                            <md-card-header-text>
                                <div class="md-title">{{layoutItems[1].header}}</div>
                                <div class="md-subhead">{{layoutItems[1].subHeader}}</div>
                            </md-card-header-text>
                                <md-card-media>
                                    <md-button class="md-raised md-primary" v-on:click="postContents">Submit</md-button>
                                </md-card-media>
                        </md-card-header>
                        <md-card-content>
                            <md-field>
                                <codemirror class="editableTextarea" v-model="layoutItems[1].vModel" :options="cmOptions"></codemirror>
                            </md-field>
                        </md-card-content>
                    </md-card>
                    
                    <md-card>
                        <md-card-header>
                            <md-card-header-text>
                                <div class="md-title">Output</div>
                                <div class="md-subhead">Test results</div>
                            </md-card-header-text>
                        </md-card-header>
                        <md-card-content>
                            <md-field>
                                <md-tabs>
                                    <md-tab id="tab-htmlResults" md-label="HTML results">
                                        <div v-html="html_result" readonly></div>
                                    </md-tab>
                                    <md-tab id="tab-pythonResults" md-label="PYTHON LOGS">
                                        <md-textarea v-model="python_result" readonly></md-textarea>
                                    </md-tab>
                                    <md-tab id="tab-textResults" md-label="OUTCOME">
                                        <md-textarea v-model="text_result" readonly></md-textarea>
                                    </md-tab>
                                </md-tabs>
                            </md-field>
                        </md-card-content>
                    </md-card>
                    
                </div>
            </div>
        </div>
        `
    })
    new Vue({
        el: '#app',
        data: function () {
            return {
                amount:0,
                questions: [
                    {
                        name: "Selecting Rows", layoutItems: [
                            { header: "Examples", subHeader: ">>> DataFrame.iloc[<row index>]", subHeader2: "NOTE: Python indexing starts from 0", vModel: "## Select the 5th row \n>>> original_df.iloc[4]\n\n## Select the first 3 rows \n>>> original_df.iloc[[0,1,2]]\n"},
                            { header: "Exercise", subHeader: 'Write your code below to modify the Original Dataframe to produce the Expected Output.', vModel: "## Select the 2nd, 5th, and 10th row \n\n" },
                            { header: "Original Dataframe", data: [{id: "1",name: "Mei Xiang",gender: "F",age:"20",children:"Yes",residence:"USA"},
                                                                    {id: "2",name: "Bei Bei",gender: "M",age:"4",children: "No",residence:"USA"},
                                                                    {id: "3",name: "Bai Yun",gender: "F",age:"28",children: "Yes",residence:"China"},
                                                                    {id: "4",name: "Bao Bao",gender: "F",age:"6",children: "No",residence:"China"},
                                                                    {id: "5",name: "Da Mao",gender: "M",age:"11",children: "No",residence:"Canada"},
                                                                    {id: "6",name: "Lin Hui",gender: "F",age:"18",children: "Yes",residence:"Thailand"},
                                                                    {id: "7",name: "Tian Tian",gender: "F",age:"16",children: "No",residence:"UK"},
                                                                    {id: "8",name: "Yuan Zai",gender: "F",age:"6",children: "No",residence:"Taiwan"},
                                                                    {id: "9",name: "Gu Gu",gender: "M",age:"20",children: "No",residence:"China"},
                                                                    {id: "10",name: "Lun Lun",gender: "F",age:"22",children: "Yes",residence:"USA"}]},
                            { header: "Expected Output", data:[{id: "2",name: "Bei Bei",gender: "M",age:"4",children: "No",residence:"USA"},
                                                                    {id: "5",name: "Da Mao",gender: "M",age:"11",children: "No",residence:"Canada"},
                                                                    {id: "10",name: "Lun Lun",gender: "F",age:"22",children: "Yes",residence:"USA"}]}
                        ], status: true
                    },
                    {
                        name: "Selecting Columns", layoutItems: [
                            { header: "Examples", subHeader: '>>> DataFrame.iloc[:,<column index>] #given index', subHeader2: ">>> DataFrame[<column name>] #given column name", vModel: "## Select the 4th column \n>>> original_df.iloc[:,3] \n \n## Select the 'AGE' column \n>>> original_df['AGE'] \n "},
                            { header: "Exercise", subHeader: 'Write your code below to modify the Original Dataframe to produce the Expected Output.', vModel: "## Select the 'ID','NAME' and 'RESIDENCE' columns\n## HINT: DataFrame[[column1,column2,..]]\n\n "},
                            { header: "Original Dataframe", data: [{id: "1",name: "Mei Xiang",gender: "F",age:"20",children:"Yes",residence:"USA"},
                                                                    {id: "2",name: "Bei Bei",gender: "M",age:"4",children: "No",residence:"USA"},
                                                                    {id: "3",name: "Bai Yun",gender: "F",age:"28",children: "Yes",residence:"China"},
                                                                    {id: "4",name: "Bao Bao",gender: "F",age:"6",children: "No",residence:"China"},
                                                                    {id: "5",name: "Da Mao",gender: "M",age:"11",children: "No",residence:"Canada"},
                                                                    {id: "6",name: "Lin Hui",gender: "F",age:"18",children: "Yes",residence:"Thailand"},
                                                                    {id: "7",name: "Tian Tian",gender: "F",age:"16",children: "No",residence:"UK"},
                                                                    {id: "8",name: "Yuan Zai",gender: "F",age:"6",children: "No",residence:"Taiwan"},
                                                                    {id: "9",name: "Gu Gu",gender: "M",age:"20",children: "No",residence:"China"},
                                                                    {id: "10",name: "Lun Lun",gender: "F",age:"22",children: "Yes",residence:"USA"}]},
                            { header: "Expected Output", data:[{id: "1",name: "Mei Xiang",residence:"USA"},
                                                                    {id: "2",name: "Bei Bei",residence:"USA"},
                                                                    {id: "3",name: "Bai Yun",residence:"China"},
                                                                    {id: "4",name: "Bao Bao",residence:"China"},
                                                                    {id: "5",name: "Da Mao",residence:"Canada"},
                                                                    {id: "6",name: "Lin Hui",residence:"Thailand"},
                                                                    {id: "7",name: "Tian Tian",residence:"UK"},
                                                                    {id: "8",name: "Yuan Zai",residence:"Taiwan"},
                                                                    {id: "9",name: "Gu Gu",residence:"China"},
                                                                    {id: "10",name: "Lun Lun",residence:"USA"}]}
                        ], status: true
                    },
                    {
                        name: "Selecting Specific Cells", layoutItems: [
                            { header: "Examples", subHeader: '>>> DataFrame.iloc[<row index>][<column index/name>]', subHeader2: "", vModel: "## Select the cell in the 3rd row and 4th column \n>>> original_df.iloc[2][3] \n \n## Select the cell in the 5th row and 'RESIDENCE' column \n>>> original_df.iloc[4]['RESIDENCE']\n " },
                            { header: "Exercise", subHeader: 'Write your code below to modify the Original Dataframe to produce the Expected Output.', vModel: "## Select the cell where 'ID'=9 and column='NAME'\n\n" },
                            { header: "Original Dataframe", data: [{id: "1",name: "Mei Xiang",gender: "F",age:"20",children:"Yes",residence:"USA"},
                                                                    {id: "2",name: "Bei Bei",gender: "M",age:"4",children: "No",residence:"USA"},
                                                                    {id: "3",name: "Bai Yun",gender: "F",age:"28",children: "Yes",residence:"China"},
                                                                    {id: "4",name: "Bao Bao",gender: "F",age:"6",children: "No",residence:"China"},
                                                                    {id: "5",name: "Da Mao",gender: "M",age:"11",children: "No",residence:"Canada"},
                                                                    {id: "6",name: "Lin Hui",gender: "F",age:"18",children: "Yes",residence:"Thailand"},
                                                                    {id: "7",name: "Tian Tian",gender: "F",age:"16",children: "No",residence:"UK"},
                                                                    {id: "8",name: "Yuan Zai",gender: "F",age:"6",children: "No",residence:"Taiwan"},
                                                                    {id: "9",name: "Gu Gu",gender: "M",age:"20",children: "No",residence:"China"},
                                                                    {id: "10",name: "Lun Lun",gender: "F",age:"22",children: "Yes",residence:"USA"}]},
                            { header: "Expected Output", data:[{name: "Gu Gu"}]}
                        ], status: true
                    },
                    {
                        name: "Replacing String Occurrences", layoutItems: [
                            { header: "Examples", subHeader: '>>> DataFrame.replace([<value>],[<replacement>])', subHeader2: "", vModel: "## Replace instances of 'USA' to 'United States'\n >>> original_df.replace(['USA'],['United States']) \n "},
                            { header: "Exercise", subHeader: 'Write your code below to modify the Original Dataframe to produce the Expected Output.', vModel: "## Replace all instances of 'F' to 'Female' and 'M' to 'Male' \n\n " },
                            { header: "Original Dataframe", data: [{id: "1",name: "Mei Xiang",gender: "F",age:"20",children:"Yes",residence:"USA"},
                                                                    {id: "2",name: "Bei Bei",gender: "M",age:"4",children: "No",residence:"USA"},
                                                                    {id: "3",name: "Bai Yun",gender: "F",age:"28",children: "Yes",residence:"China"},
                                                                    {id: "4",name: "Bao Bao",gender: "F",age:"6",children: "No",residence:"China"},
                                                                    {id: "5",name: "Da Mao",gender: "M",age:"11",children: "No",residence:"Canada"},
                                                                    {id: "6",name: "Lin Hui",gender: "F",age:"18",children: "Yes",residence:"Thailand"},
                                                                    {id: "7",name: "Tian Tian",gender: "F",age:"16",children: "No",residence:"UK"},
                                                                    {id: "8",name: "Yuan Zai",gender: "F",age:"6",children: "No",residence:"Taiwan"},
                                                                    {id: "9",name: "Gu Gu",gender: "M",age:"20",children: "No",residence:"China"},
                                                                    {id: "10",name: "Lun Lun",gender: "F",age:"22",children: "Yes",residence:"USA"}]},
                            { header: "Expected Output", data:[{id: "1",name: "Mei Xiang",gender: "F",age:"20",children:"Yes",residence:"United States"},
                                                                    {id: "2",name: "Bei Bei",gender: "M",age:"4",children: "No",residence:"United States"},
                                                                    {id: "3",name: "Bai Yun",gender: "F",age:"28",children: "Yes",residence:"China"},
                                                                    {id: "4",name: "Bao Bao",gender: "F",age:"6",children: "No",residence:"China"},
                                                                    {id: "5",name: "Da Mao",gender: "M",age:"11",children: "No",residence:"Canada"},
                                                                    {id: "6",name: "Lin Hui",gender: "F",age:"18",children: "Yes",residence:"Thailand"},
                                                                    {id: "7",name: "Tian Tian",gender: "F",age:"16",children: "No",residence:"UK"},
                                                                    {id: "8",name: "Yuan Zai",gender: "F",age:"6",children: "No",residence:"Taiwan"},
                                                                    {id: "9",name: "Gu Gu",gender: "M",age:"20",children: "No",residence:"China"},
                                                                    {id: "10",name: "Lun Lun",gender: "F",age:"22",children: "Yes",residence:"United States"}]}
                        ], status: true
                    },
                    {
                        name: "Filtering Data in Columns", layoutItems: [
                            { header: "Examples", subHeader: '>>> DataFrame[<boolean condition>]', subHeader2: "", vModel: "## Filter for female pandas only \n>>> original_df = original_df[original_df['GENDER']=='F'] \n \n## Filter for pandas living in the USA \n>>> original_df = original_df[original_df['RESIDENCE']=='USA']\n " },
                            { header: "Exercise", subHeader: 'Write your code below to modify the Original Dataframe to produce the Expected Output.', vModel: "## Filter for pandas with children \n\n" },
                            { header: "Original Dataframe", data: [{id: "1",name: "Mei Xiang",gender: "F",age:"20",children:"Yes",residence:"USA"},
                                                                    {id: "2",name: "Bei Bei",gender: "M",age:"4",children: "No",residence:"USA"},
                                                                    {id: "3",name: "Bai Yun",gender: "F",age:"28",children: "Yes",residence:"China"},
                                                                    {id: "4",name: "Bao Bao",gender: "F",age:"6",children: "No",residence:"China"},
                                                                    {id: "5",name: "Da Mao",gender: "M",age:"11",children: "No",residence:"Canada"},
                                                                    {id: "6",name: "Lin Hui",gender: "F",age:"18",children: "Yes",residence:"Thailand"},
                                                                    {id: "7",name: "Tian Tian",gender: "F",age:"16",children: "No",residence:"UK"},
                                                                    {id: "8",name: "Yuan Zai",gender: "F",age:"6",children: "No",residence:"Taiwan"},
                                                                    {id: "9",name: "Gu Gu",gender: "M",age:"20",children: "No",residence:"China"},
                                                                    {id: "10",name: "Lun Lun",gender: "F",age:"22",children: "Yes",residence:"USA"}]},
                            { header: "Expected Output", data: [{id: "1",name: "Mei Xiang",gender: "F",age:"20",children:"Yes",residence:"USA"},
                                                                    {id: "3",name: "Bai Yun",gender: "F",age:"28",children: "Yes",residence:"China"},
                                                                    {id: "6",name: "Lin Hui",gender: "F",age:"18",children: "Yes",residence:"Thailand"},
                                                                    {id: "10",name: "Lun Lun",gender: "F",age:"22",children: "Yes",residence:"USA"}]}
                        ], status: true
                    },
                    {
                        name: "Filtering Data based on Multiple Conditions", layoutItems: [
                            { header: "Examples", subHeader: ">>> DataFrame[<boolean condition1><operator><boolean condition2]", subHeader2: "AND: &, OR: |, NOT: ~", vModel: "## Filter for FEMALE pandas YOUNGER than 10 years old \n>>> original_df[(original_df['GENDER']=='F') \n   &(original_df['AGE']<10)]\n "},
                            { header: "Exercise", subHeader: 'Write your code below to modify the Original Dataframe to produce the Expected Output.', vModel: "## Filter for pandas OLDER than 15 years old OR that live in China \n\n "},
                            { header: "Original Dataframe", data: [{id: "1",name: "Mei Xiang",gender: "F",age:"20",children:"Yes",residence:"USA"},
                                                                    {id: "2",name: "Bei Bei",gender: "M",age:"4",children: "No",residence:"USA"},
                                                                    {id: "3",name: "Bai Yun",gender: "F",age:"28",children: "Yes",residence:"China"},
                                                                    {id: "4",name: "Bao Bao",gender: "F",age:"6",children: "No",residence:"China"},
                                                                    {id: "5",name: "Da Mao",gender: "M",age:"11",children: "No",residence:"Canada"},
                                                                    {id: "6",name: "Lin Hui",gender: "F",age:"18",children: "Yes",residence:"Thailand"},
                                                                    {id: "7",name: "Tian Tian",gender: "F",age:"16",children: "No",residence:"UK"},
                                                                    {id: "8",name: "Yuan Zai",gender: "F",age:"6",children: "No",residence:"Taiwan"},
                                                                    {id: "9",name: "Gu Gu",gender: "M",age:"20",children: "No",residence:"China"},
                                                                    {id: "10",name: "Lun Lun",gender: "F",age:"22",children: "Yes",residence:"USA"}]},
                            { header: "Expected Output", data:[{id: "1",name: "Mei Xiang",gender: "F",age:"20",children:"Yes",residence:"USA"},
                                                                    {id: "3",name: "Bai Yun",gender: "F",age:"28",children: "Yes",residence:"China"},
                                                                    {id: "4",name: "Bao Bao",gender: "F",age:"6",children: "No",residence:"China"},
                                                                    {id: "6",name: "Lin Hui",gender: "F",age:"18",children: "Yes",residence:"Thailand"},
                                                                    {id: "9",name: "Gu Gu",gender: "M",age:"20",children: "No",residence:"China"},
                                                                    {id: "10",name: "Lun Lun",gender: "F",age:"22",children: "Yes",residence:"USA"}]}
                        ], status: true
                    },
                    {
                        name: "Adding Rows", layoutItems: [
                            { header: "Examples", subHeader: 'Objective: Learn how to add new data rows into dataframe', subHeader2: "", vModel: "## Add a new row to the dataframe \n>>> original_df = original_df.append(pd.Series([15,'Ming Ming', 'F', 6, 'No', 'Australia'], index=original_df.columns), ignore_index=True)\n "},
                            { header: "Exercise", subHeader: 'Write your code below to modify the Original Dataframe to produce the Expected Output.', vModel: "## Add a new row to the dataframe with the following values: \n## ID:11, Name:Tao Tao, Gender:M, Age:20, Children:Yes, Residence:Singapore\n\n "},
                            { header: "Original Dataframe", data: [{id: "1",name: "Mei Xiang",gender: "F",age:"20",children:"Yes",residence:"USA"},
                                                                    {id: "2",name: "Bei Bei",gender: "M",age:"4",children: "No",residence:"USA"},
                                                                    {id: "3",name: "Bai Yun",gender: "F",age:"28",children: "Yes",residence:"China"},
                                                                    {id: "4",name: "Bao Bao",gender: "F",age:"6",children: "No",residence:"China"},
                                                                    {id: "5",name: "Da Mao",gender: "M",age:"11",children: "No",residence:"Canada"},
                                                                    {id: "6",name: "Lin Hui",gender: "F",age:"18",children: "Yes",residence:"Thailand"},
                                                                    {id: "7",name: "Tian Tian",gender: "F",age:"16",children: "No",residence:"UK"},
                                                                    {id: "8",name: "Yuan Zai",gender: "F",age:"6",children: "No",residence:"Taiwan"},
                                                                    {id: "9",name: "Gu Gu",gender: "M",age:"20",children: "No",residence:"China"},
                                                                    {id: "10",name: "Lun Lun",gender: "F",age:"22",children: "Yes",residence:"USA"}]},
                            { header: "Expected Output", data:[{id: "1",name: "Mei Xiang",gender: "F",age:"20",children:"Yes",residence:"USA"},
                                                                    {id: "2",name: "Bei Bei",gender: "M",age:"4",children: "No",residence:"USA"},
                                                                    {id: "3",name: "Bai Yun",gender: "F",age:"28",children: "Yes",residence:"China"},
                                                                    {id: "4",name: "Bao Bao",gender: "F",age:"6",children: "No",residence:"China"},
                                                                    {id: "5",name: "Da Mao",gender: "M",age:"11",children: "No",residence:"Canada"},
                                                                    {id: "6",name: "Lin Hui",gender: "F",age:"18",children: "Yes",residence:"Thailand"},
                                                                    {id: "7",name: "Tian Tian",gender: "F",age:"16",children: "No",residence:"UK"},
                                                                    {id: "8",name: "Yuan Zai",gender: "F",age:"6",children: "No",residence:"Taiwan"},
                                                                    {id: "9",name: "Gu Gu",gender: "M",age:"20",children: "No",residence:"China"},
                                                                    {id: "10",name: "Lun Lun",gender: "F",age:"22",children: "Yes",residence:"USA"},
                                                                    {id: "11",name: "Tao Tao",gender: "M",age:"20",children: "Yes",residence:"Singapore"}]}
                        ], status: true
                    },
                    {
                        name: "Deleting Rows", layoutItems: [
                            { header: "Examples", subHeader: 'Objective: Learn how to delete rows from dataframe', subHeader2: "", vModel: "## Deleting second row from the dataframe \n>>> original_df = original_df.drop(original_df.index[1])\n "},
                            { header: "Exercise", subHeader: 'Write your code below to modify the Original Dataframe to produce the Expected Output.', vModel: "## Delete fifth and tenth rows from the dataframe\n\n "},
                            { header: "Original Dataframe", data: [{id: "1",name: "Mei Xiang",gender: "F",age:"20",children:"Yes",residence:"USA"},
                                                                    {id: "2",name: "Bei Bei",gender: "M",age:"4",children: "No",residence:"USA"},
                                                                    {id: "3",name: "Bai Yun",gender: "F",age:"28",children: "Yes",residence:"China"},
                                                                    {id: "4",name: "Bao Bao",gender: "F",age:"6",children: "No",residence:"China"},
                                                                    {id: "5",name: "Da Mao",gender: "M",age:"11",children: "No",residence:"Canada"},
                                                                    {id: "6",name: "Lin Hui",gender: "F",age:"18",children: "Yes",residence:"Thailand"},
                                                                    {id: "7",name: "Tian Tian",gender: "F",age:"16",children: "No",residence:"UK"},
                                                                    {id: "8",name: "Yuan Zai",gender: "F",age:"6",children: "No",residence:"Taiwan"},
                                                                    {id: "9",name: "Gu Gu",gender: "M",age:"20",children: "No",residence:"China"},
                                                                    {id: "10",name: "Lun Lun",gender: "F",age:"22",children: "Yes",residence:"USA",}]},
                            { header: "Expected Output", data:[{id: "1",name: "Mei Xiang",gender: "F",age:"20",children:"Yes",residence:"USA"},
                                                                    {id: "2",name: "Bei Bei",gender: "M",age:"4",children: "No",residence:"USA"},
                                                                    {id: "3",name: "Bai Yun",gender: "F",age:"28",children: "Yes",residence:"China"},
                                                                    {id: "4",name: "Bao Bao",gender: "F",age:"6",children: "No",residence:"China"},
                                                                    {id: "6",name: "Lin Hui",gender: "F",age:"18",children: "Yes",residence:"Thailand"},
                                                                    {id: "7",name: "Tian Tian",gender: "F",age:"16",children: "No",residence:"UK"},
                                                                    {id: "8",name: "Yuan Zai",gender: "F",age:"6",children: "No",residence:"Taiwan"},
                                                                    {id: "9",name: "Gu Gu",gender: "M",age:"20",children: "No",residence:"China"}]}
                        ], status: true
                    },
                    {
                        name: "Finding Min and Max", layoutItems: [
                            { header: "Examples", subHeader: 'Objective: Learn how to find Min and Max values in column', subHeader2: "", vModel: "## Find the minimum value of column 'Age' \n>>> original_df = original_df['AGE'].min()\n\n## Find the maximum value of column 'NAME' \n>>> original_df = original_df['NAME'].max() \n" },
                            { header: "Exercise", subHeader: 'Write your code below to modify the Original Dataframe to produce the Expected Output.', vModel: "## Find the minimum value of column 'Name' \n\n"},
                            { header: "Original Dataframe", data: [{id: "1",name: "Mei Xiang",gender: "F",age:"20",children:"Yes",residence:"USA"},
                                                                    {id: "2",name: "Bei Bei",gender: "M",age:"4",children: "No",residence:"USA"},
                                                                    {id: "3",name: "Bai Yun",gender: "F",age:"28",children: "Yes",residence:"China"},
                                                                    {id: "4",name: "Bao Bao",gender: "F",age:"6",children: "No",residence:"China"},
                                                                    {id: "5",name: "Da Mao",gender: "M",age:"11",children: "No",residence:"Canada"},
                                                                    {id: "6",name: "Lin Hui",gender: "F",age:"18",children: "Yes",residence:"Thailand"},
                                                                    {id: "7",name: "Tian Tian",gender: "F",age:"16",children: "No",residence:"UK"},
                                                                    {id: "8",name: "Yuan Zai",gender: "F",age:"6",children: "No",residence:"Taiwan"},
                                                                    {id: "9",name: "Gu Gu",gender: "M",age:"20",children: "No",residence:"China"},
                                                                    {id: "10",name: "Lun Lun",gender: "F",age:"22",children: "Yes",residence:"USA"}]},
                            { header: "Expected Output", data:[{name: "Bai Yun"}]}
                        ], status: true
                    },
                    {
                        name: "Multiplying and Dividing Column values", layoutItems: [
                            { header: "Examples", subHeader: 'Objective: Learn how to multiply and divide column values', subHeader2: "", vModel: "## Multiply all the values in column 'ID' by 2 \n>>> original_df = original_df['ID']*=2 \n\n" },
                            { header: "Exercise", subHeader: 'Write your code below to modify the Original Dataframe to produce the Expected Output.', vModel: "## Multiply all the values in column 'age' by 10 \n\n" },
                            { header: "Original Dataframe", data: [{id: "1",name: "Mei Xiang",gender: "F",age:"20",children:"Yes",residence:"USA"},
                                                                    {id: "2",name: "Bei Bei",gender: "M",age:"4",children: "No",residence:"USA"},
                                                                    {id: "3",name: "Bai Yun",gender: "F",age:"28",children: "Yes",residence:"China"},
                                                                    {id: "4",name: "Bao Bao",gender: "F",age:"6",children: "No",residence:"China"},
                                                                    {id: "5",name: "Da Mao",gender: "M",age:"11",children: "No",residence:"Canada"},
                                                                    {id: "6",name: "Lin Hui",gender: "F",age:"18",children: "Yes",residence:"Thailand"},
                                                                    {id: "7",name: "Tian Tian",gender: "F",age:"16",children: "No",residence:"UK"},
                                                                    {id: "8",name: "Yuan Zai",gender: "F",age:"6",children: "No",residence:"Taiwan"},
                                                                    {id: "9",name: "Gu Gu",gender: "M",age:"20",children: "No",residence:"China"},
                                                                    {id: "10",name: "Lun Lun",gender: "F",age:"22",children: "Yes",residence:"USA"}]},
                            { header: "Expected Output", data:[{id: "1",name: "Mei Xiang",gender: "F",age:"40",children:"Yes",residence:"USA"},
                                                                    {id: "2",name: "Bei Bei",gender: "M",age:"8",children: "No",residence:"USA"},
                                                                    {id: "3",name: "Bai Yun",gender: "F",age:"56",children: "Yes",residence:"China"},
                                                                    {id: "4",name: "Bao Bao",gender: "F",age:"12",children: "No",residence:"China"},
                                                                    {id: "5",name: "Da Mao",gender: "M",age:"22",children: "No",residence:"Canada"},
                                                                    {id: "6",name: "Lin Hui",gender: "F",age:"36",children: "Yes",residence:"Thailand"},
                                                                    {id: "7",name: "Tian Tian",gender: "F",age:"32",children: "No",residence:"UK"},
                                                                    {id: "8",name: "Yuan Zai",gender: "F",age:"12",children: "No",residence:"Taiwan"},
                                                                    {id: "9",name: "Gu Gu",gender: "M",age:"40",children: "No",residence:"China"},
                                                                    {id: "10",name: "Lun Lun",gender: "F",age:"44",children: "Yes",residence:"USA"}]}
                        ], status: true
                    },
                ]
            }
        },
        methods: {
            updateProgress(progress){
                this.amount = progress;
            }
        }
    })
    
</script>

<style lang="scss" scoped>
    .title-name{
        text-align: center;
        font-size: 40px;
        height: 40px;
        margin: 15px;
    }
    .md-stepper-header{
        height: 24px
        
    }
    .md-card {
        width: 95%;
        margin: 0px;
        display: inline-block;
        vertical-align: top;
        min-height: 50px;
        max-height: 400px
    }
    .md-card-content {
        padding-bottom: 16px !important;
    }
    button {
        display: block;
        margin: 20px 60px 20px 60px;
        width: 200px !important;
    }
    #cardGroupCreator {
        display: flex;
        flex-direction: column;
        padding-right: 0px
    }
    #cardGroupPreview .md-card {
        width: 100%;
    }
    #cardGroupPreview {
        padding-left: 0px
    }
    #cardGroupPreview .md-tab {
        height: 100%
    }
    textarea {
        font-size: 1rem !important;
        min-height: 175px !important
    }
    .md-tabs {
        width: 100%;
    }
    .md-tab {
        overflow-x: auto;
    }
    .md-tab::-webkit-scrollbar {
        width: 0px;
    }
    html {
        width: 95%;
        margin: auto;
        mix-blend-mode: darken
    }
    h1 {
        background: #EDBC00;
        color: #111;
        font-family: 'Helvetica Neue', sans-serif; 
        font-size: 40px; 
        padding: 12px;
        font-weight: bold; 
        letter-spacing: -1px; 
        line-height: 1;
        margin: auto;
        text-align: center
    }
    .md-content {
        min-height: 300px
    }
    .md-tabs-container,
    .md-tabs-container .md-tab textarea,
    .md-tabs-content {
        height: 100% !important
    }
    .md-field {
        margin: 0px;
        padding: 0px
    }
    .md-tabs-navigation {
        justify-content: center !important
    }
    .md-card-media {
        width: 400px !important
    }
    .md-button {
        margin: 10px !important
    }
    .cm-s-default {
        height: 100%
    }
    .md-card-header {
        padding: 0 16px 16px 16px
    }
</style>

</html>
