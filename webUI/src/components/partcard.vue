<template>
    <a-list item-layout="vertical" size="large" :pagination="pagination" :data-source="listData">
        <a-list-item slot="renderItem" :key="index" slot-scope="item,index">
            <a-list-item-meta>
                <div slot="description">
                    <a-tag color="pink">
                        Year: {{item.year}}
                    </a-tag>
                    <a-tag color="green">
                        Team: {{item.team}}
                    </a-tag>
                    <a-tag color="cyan">
                        Designer: {{item.designer}}
                    </a-tag>
                    <a-tag color="blue">
                        Type: {{item.type}}
                    </a-tag>
                </div>
                <a slot="title" style="color: #e37654" @click="handleClick(item.number)">{{item.number}}: {{item.name}}</a>
            </a-list-item-meta>
            <p v-html="highlight(item.matchedContents)"></p>
            <p style="color: gray">{{item.cites}} cited · {{item.twins_num}} twin(s) · {{item.length}} bp · {{item.isfavorite ==='True' ? 'Favorite Part · ':''}}
            {{item.released ==='Not Released' ? item.released+' · ':''}}{{item.date}}  <a target="_blank" :href="item.url">View in iGEM Parts Registry</a>
            </p>
        </a-list-item>
    </a-list>
</template>
<script>
export default {
    props:['listData','searchQuery'],
    data(){
        return{
            pagination: {
                onChange: page => {
                    console.log(page);
                },
                pageSize: 10,
            },
        }
    },
    methods:{
        highlight(content){
            if (content==='nan'){
                return '';
            }
            const regex = new RegExp(this.searchQuery, "gi");
            try{
                return content.replace(regex, '<span style="color:red;">$&</span>') + '...';
            } catch (error){
                return content + '...';
            }
        },
        handleClick(number){
            this.$emit('clickTitle',number);
        },
    }
}
</script>
<style scoped>
</style>