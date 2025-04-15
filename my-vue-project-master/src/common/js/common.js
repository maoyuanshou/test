// 自定义加密算法
export function customEncrypt(password, key) {
  let encrypted = [];
  for (let i = 0; i < password.length; i++) {
      // 使用密钥的循环字符进行异或操作
      let keyChar = key[i % key.length];
      encrypted.push(String.fromCharCode(password.charCodeAt(i) ^ keyChar.charCodeAt(0)));
  }
  return encrypted.join("");
}

// 自定义解密算法（与加密算法相同）
export function customDecrypt(encrypted, key) {
  return customEncrypt(encrypted, key); // 异或操作的特性：加密和解密相同
}

export const secretKey = "pipeline"; // 密钥