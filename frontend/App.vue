<template>
  <div style="max-width: 600px; margin: 40px auto; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px #eee; background: #fff;">
    <h2 style="text-align:center;">AI 对话演示</h2>
    <div v-for="(msg, idx) in messages" :key="idx" :style="msg.role==='user'?userStyle:aiStyle">
      <b>{{ msg.role === 'user' ? '你' : 'AI' }}：</b>{{ msg.content }}
    </div>
    <div style="display:flex; margin-top:20px;">
      <input v-model="input" @keyup.enter="send" placeholder="请输入内容..." style="flex:1; padding:8px; border-radius:4px; border:1px solid #ddd;" />
      <button @click="send" :disabled="loading || !input.trim()" style="margin-left:8px; padding:8px 16px;">发送</button>
    </div>
    <div v-if="loading" style="color:#888; margin-top:10px;">AI 正在思考...</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const input = ref('')
const messages = ref([])
const loading = ref(false)

const userStyle = {
  background: '#e6f7ff',
  padding: '8px',
  borderRadius: '6px',
  margin: '8px 0',
}
const aiStyle = {
  background: '#f6ffed',
  padding: '8px',
  borderRadius: '6px',
  margin: '8px 0',
}

async function send() {
  if (!input.value.trim() || loading.value) return
  messages.value.push({ role: 'user', content: input.value })
  const history = messages.value.slice(-10) // 只保留最近10条上下文
  input.value = ''
  loading.value = true
  try {
    const res = await axios.post('/chat', {
      messages: history
    })
    messages.value.push({ role: 'assistant', content: res.data.reply })
  } catch (e) {
    messages.value.push({ role: 'assistant', content: 'AI接口请求失败' })
  } finally {
    loading.value = false
  }
}
</script>

<style>
body {
  background: #f5f5f5;
}
</style>