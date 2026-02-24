import { Message } from "../messages/messages";

// ==========================================
//在此处修改你的 Ollama 模型名称
// 例如: "qwen2.5", "llama3", "gemma2", "deepseek-r1"
const OLLAMA_MODEL = "qwen3:1.7b"; 
// ==========================================

export async function getChatResponse(messages: Message[], apiKey: string) {
  // Ollama 不需要真实的 Key，但为了通过 ChatVRM 的逻辑，这里不做强校验
  // 或者你可以在这里写死 apiKey = "ollama"
  
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    // 即使是本地，保持这个 Header 格式比较好，随便填什么都行
    Authorization: `Bearer ${apiKey || "ollama"}`,
  };

  try {
    const res = await fetch("http://localhost:11434/v1/chat/completions", {
      headers: headers,
      method: "POST",
      body: JSON.stringify({
        model: OLLAMA_MODEL,
        messages: messages,
        stream: false, // 非流式
        max_tokens: 2048,
      }),
    });

    if (!res.ok) {
      throw new Error(`Ollama API Error: ${res.status} ${res.statusText}`);
    }

    const data = await res.json();
    const message = data.choices[0]?.message?.content || "无回复";

    return { message: message };
  } catch (e) {
    console.error(e);
    return { message: "连接本地 Ollama 失败，请检查是否运行了 ollama serve" };
  }
}

export async function getChatResponseStream(
  messages: Message[],
  apiKey: string
) {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${apiKey || "ollama"}`,
  };

  const res = await fetch("http://localhost:11434/v1/chat/completions", {
    headers: headers,
    method: "POST",
    body: JSON.stringify({
      model: OLLAMA_MODEL,
      messages: messages,
      stream: true, // 开启流式
      max_tokens: 200,
    }),
  });

  const reader = res.body?.getReader();
  if (res.status !== 200 || !reader) {
    throw new Error(`Ollama API Error: ${res.status} ${res.statusText}`);
  }

  const stream = new ReadableStream({
    async start(controller: ReadableStreamDefaultController) {
      const decoder = new TextDecoder("utf-8");
      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          
          const data = decoder.decode(value, { stream: true });
          
          // Ollama 的流式返回格式兼容 OpenAI，通常以 "data: " 开头
          const chunks = data
            .split("\n") // Ollama 有时会用换行符分割
            .filter((val) => !!val && val.trim() !== "");

          for (const chunk of chunks) {
            // 处理结束标记
            if (chunk.includes("[DONE]")) continue;

            // 移除 "data: " 前缀
            const jsonStr = chunk.replace(/^data: /, "").trim();
            if (!jsonStr) continue;

            try {
              const json = JSON.parse(jsonStr);
              const messagePiece = json.choices[0]?.delta?.content;
              if (!!messagePiece) {
                controller.enqueue(messagePiece);
              }
            } catch (error) {
              // 忽略 JSON 解析错误（防止某个数据包不完整导致整个流断开）
              console.warn("JSON parse error in stream:", error);
            }
          }
        }
      } catch (error) {
        controller.error(error);
      } finally {
        reader.releaseLock();
        controller.close();
      }
    },
  });

  return stream;
}
