# Ôn tập phỏng vấn: Linked List + Stack/Queue (Ưu tiên trung bình)

> Nhóm này Zalo (và nhiều công ty) hay hỏi ở mức "kiểm tra nền tảng cấu trúc dữ liệu" — thường không khó thuật toán, nhưng dễ sai ở việc **quản lý con trỏ** (pointer). Interviewer sẽ chú ý cách bạn xử lý edge case (list rỗng, 1 node) và code có gọn/không lỗi off-by-one.

---

# PHẦN 1: LINKED LIST

## 1. Reverse Linked List

### Đề bài
Cho `head` của một singly linked list. Đảo ngược thứ tự các node và trả về `head` mới.

**Ví dụ:** `1 -> 2 -> 3 -> 4 -> 5 -> None` → `5 -> 4 -> 3 -> 2 -> 1 -> None`

### Hướng làm
- **Cách 1 — Iterative (khuyên dùng khi phỏng vấn, O(n) time, O(1) space):**
  - Giữ 3 con trỏ: `prev` (node trước, ban đầu = None), `curr` (node hiện tại, ban đầu = head), `next_temp` (lưu tạm node kế tiếp trước khi đổi hướng).
  - Tại mỗi bước: lưu `next_temp = curr.next`, đảo hướng `curr.next = prev`, rồi dịch `prev = curr`, `curr = next_temp`.
  - Lặp đến khi `curr == None`. Lúc đó `prev` chính là head mới.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseList(head):
    prev = None
    curr = head
    while curr:
        next_temp = curr.next   # lưu lại trước khi mất
        curr.next = prev        # đảo hướng
        prev = curr             # dịch prev lên
        curr = next_temp        # dịch curr lên
    return prev  # prev chính là head mới
```

- **Cách 2 — Recursive (O(n) time, O(n) space do call stack):**

```python
def reverseList(head):
    if not head or not head.next:
        return head
    new_head = reverseList(head.next)
    head.next.next = head   # node kế tiếp trỏ ngược lại head
    head.next = None        # cắt đường link cũ
    return new_head
```

### Cách trình bày khi phỏng vấn
1. Vẽ hình minh họa từng bước trên giấy/bảng — bài này cực kỳ dễ nói nhầm nếu không vẽ ra, vì phải đổi hướng 3 con trỏ cùng lúc.
2. Giải thích rõ **tại sao cần biến `next_temp`**: "Nếu đảo `curr.next = prev` trước mà chưa lưu `curr.next` cũ, mình sẽ mất luôn phần còn lại của list."
3. Nêu cả 2 cách (iterative và recursive), giải thích trade-off: iterative O(1) space tốt hơn, nhưng recursive code ngắn gọn hơn và thể hiện tư duy đệ quy tốt — nói rõ bạn biết cả 2 và **chọn iterative làm chính** vì tiết kiệm bộ nhớ.
4. Dry-run với list nhỏ `1->2->3` để chứng minh đúng, đặc biệt kiểm tra edge case: list rỗng (`head = None`) và list 1 node.
5. Follow-up hay gặp: "Đảo ngược 1 đoạn con của list (Reverse Linked List II)" hoặc "Đảo ngược theo từng nhóm k node (Reverse Nodes in k-Group)" — biết tên để không bị bất ngờ nếu hỏi thêm.

---

## 2. Detect Cycle (Floyd's Cycle Detection / "Tortoise and Hare")

### Đề bài
Cho `head` của linked list, xác định list có chứa **chu trình (cycle)** không — tức có node nào mà đi theo `next` liên tục sẽ quay lại chính nó.

**Ví dụ:** list `3 -> 2 -> 0 -> -4` mà node `-4` trỏ ngược về node `2` → có cycle → `true`

### Hướng làm
- **Cách dễ nghĩ nhưng tốn space — Hash Set (O(n) space):** duyệt qua từng node, lưu vào set; nếu gặp node đã có trong set → có cycle. Nên nhắc cách này trước, nhưng chỉ ra nhược điểm về space.
- **Cách tối ưu — Floyd's Cycle Detection (2 con trỏ nhanh/chậm, O(1) space):**
  - Dùng 2 con trỏ: `slow` đi 1 bước mỗi lần, `fast` đi 2 bước mỗi lần, cả 2 bắt đầu từ `head`.
  - Nếu list **không có cycle**, `fast` sẽ chạy đến `None` trước.
  - Nếu list **có cycle**, `fast` và `slow` chắc chắn sẽ **gặp nhau** tại một điểm nào đó bên trong vòng lặp (giống 2 người chạy trên đường đua vòng tròn với tốc độ khác nhau, người nhanh sẽ "vòng lại" và đuổi kịp người chậm).

```python
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

### Cách trình bày khi phỏng vấn
1. Nêu insight cốt lõi bằng ví dụ đời thường: "Giống như 2 người chạy vòng quanh 1 đường đua tròn, người chạy nhanh gấp đôi chắc chắn sẽ 'vòng qua' và gặp lại người chạy chậm nếu đường đua là vòng kín. Nếu đường thẳng (không cycle), người nhanh sẽ về đích trước, không bao giờ gặp lại."
2. Giải thích điều kiện vòng lặp `while fast and fast.next` — vì sao cần check cả 2: tránh lỗi truy cập `None.next` khi `fast` đã chạm cuối list.
3. Nhấn mạnh ưu điểm: O(1) space so với hash set O(n) — đây chính là lý do thuật toán này được ưa chuộng trong phỏng vấn.
4. Follow-up rất hay gặp: **"Tìm node bắt đầu của cycle (không chỉ có/không)"** — đây là phần 2 của bài (LeetCode 142). Ý tưởng: sau khi `slow` và `fast` gặp nhau, đặt 1 con trỏ mới tại `head`, giữ nguyên `slow` tại điểm gặp, cho cả 2 cùng đi 1 bước mỗi lần — điểm chúng gặp nhau tiếp theo chính là **node bắt đầu cycle**. Đây là chứng minh toán học (dựa vào khoảng cách), nên biết trước để không bị bất ngờ.
5. Follow-up khác: "Tìm độ dài cycle?" → sau khi 2 con trỏ gặp nhau, giữ 1 con trỏ đứng yên, cho con trỏ kia chạy tiếp đến khi gặp lại → số bước đi được chính là độ dài cycle.

---

## 3. Merge Two Sorted Lists

### Đề bài
Cho `head` của 2 linked list đã sort tăng dần (`list1`, `list2`). Gộp thành 1 list sort tăng dần duy nhất bằng cách nối các node có sẵn (không tạo node mới), trả về `head` của list gộp.

**Ví dụ:** `list1 = 1->2->4`, `list2 = 1->3->4` → `1->1->2->3->4->4`

### Hướng làm
- Dùng kỹ thuật **Dummy Node (node giả)** để đơn giản hóa việc xử lý head — tránh phải viết code riêng cho trường hợp "node đầu tiên của kết quả".
- Dùng 1 con trỏ `tail` chạy theo, luôn nối node nhỏ hơn giữa `list1` và `list2` vào sau `tail`, rồi dịch con trỏ tương ứng tiến lên.
- Sau khi 1 trong 2 list hết, nối phần còn lại của list kia vào (vì đã sort sẵn, không cần duyệt tiếp).

```python
def mergeTwoLists(list1, list2):
    dummy = ListNode()
    tail = dummy

    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next

    # nối phần còn lại (chỉ 1 trong 2 còn node, không cả 2)
    tail.next = list1 if list1 else list2

    return dummy.next
```

### Cách trình bày khi phỏng vấn
1. Giới thiệu kỹ thuật **Dummy Node** ngay từ đầu: "Mình dùng 1 node giả (dummy) để làm điểm bắt đầu, giúp code không cần xử lý riêng trường hợp gán head lần đầu — cuối cùng chỉ cần trả về `dummy.next`." Đây là kỹ thuật rất phổ biến trong bài Linked List, nên nhắc rõ vì nó thể hiện bạn biết pattern chuẩn.
2. Nhấn mạnh: bài này **không tạo node mới**, chỉ nối lại các node có sẵn bằng cách thay đổi con trỏ `next` — tiết kiệm bộ nhớ.
3. Giải thích dòng cuối `tail.next = list1 if list1 else list2`: vì 1 trong 2 list đã hết trước, phần còn lại của list kia **chắc chắn đã sort sẵn**, nên chỉ cần nối thẳng vào mà không cần duyệt từng node.
4. Độ phức tạp: Time O(n + m) (n, m là độ dài 2 list), Space O(1) ngoài dummy node.
5. Follow-up rất hay gặp ở Zalo/nhiều công ty: **"Merge k Sorted Lists"** — mở rộng từ 2 lên k list, dùng Min-Heap hoặc merge từng cặp theo kiểu divide-and-conquer (O(n log k)) — nên biết hướng để không bị động nếu bị hỏi tiếp.

---

# PHẦN 2: STACK / QUEUE

## 4. Valid Parentheses
*(Đã trình bày chi tiết ở phần String cơ bản — xem lại: dùng Stack, đẩy ngoặc mở, pop và so khớp khi gặp ngoặc đóng, cuối cùng stack phải rỗng.)*

**Nhắc nhanh điểm chốt để ôn lại:**
- Stack phù hợp vì tính chất LIFO — ngoặc đóng phải khớp với ngoặc mở **gần nhất chưa đóng**.
- 3 case sai: stack rỗng khi gặp ngoặc đóng, không khớp loại ngoặc, hoặc còn dư ngoặc mở sau khi duyệt hết.
- Time O(n), Space O(n).

---

## 5. Implement Queue using Stacks

### Đề bài
Cài đặt một **Queue (FIFO — vào trước ra trước)** chỉ bằng cách sử dụng **2 Stack** (LIFO — vào sau ra trước). Cần hỗ trợ các thao tác: `push(x)`, `pop()`, `peek()`, `empty()`.

### Hướng làm
Đây là bài kinh điển để test hiểu biết sâu về sự khác biệt giữa Stack và Queue, và cách "giả lập" cấu trúc này bằng cấu trúc kia.

- **Ý tưởng cốt lõi:** dùng 2 stack — `stack_in` (dùng để push vào) và `stack_out` (dùng để pop/peek ra).
  - `push(x)`: luôn đẩy vào `stack_in` — đơn giản, O(1).
  - `pop()` / `peek()`: nếu `stack_out` đang **rỗng**, đổ hết `stack_in` sang `stack_out` (bằng cách pop từng phần tử từ `stack_in`, push vào `stack_out`) — thao tác đổ này **đảo ngược thứ tự**, biến LIFO thành FIFO đúng như mong muốn. Sau đó pop/peek từ `stack_out`.
  - Nếu `stack_out` **không rỗng** → không cần đổ lại, pop/peek trực tiếp từ `stack_out` luôn (vì thứ tự đã đúng từ lần đổ trước).

```python
class MyQueue:
    def __init__(self):
        self.stack_in = []
        self.stack_out = []

    def push(self, x):
        self.stack_in.append(x)

    def _transfer_if_needed(self):
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())

    def pop(self):
        self._transfer_if_needed()
        return self.stack_out.pop()

    def peek(self):
        self._transfer_if_needed()
        return self.stack_out[-1]

    def empty(self):
        return not self.stack_in and not self.stack_out
```

### Cách trình bày khi phỏng vấn
1. Giải thích trực quan bằng ví dụ: "Nếu push 1, 2, 3 vào 1 stack, pop ra sẽ được 3, 2, 1 (ngược lại thứ tự mong muốn của queue). Nhưng nếu đổ (pop hết rồi push) toàn bộ stack đó sang 1 stack thứ 2, thứ tự sẽ bị **đảo lại lần nữa** → 1, 2, 3 — đúng thứ tự FIFO cần có."
2. Nhấn mạnh **tối ưu quan trọng nhất của bài này — Amortized O(1)**: "Mình chỉ đổ từ `stack_in` sang `stack_out` khi `stack_out` rỗng, KHÔNG đổ mỗi lần gọi pop/peek. Điều này đảm bảo mỗi phần tử chỉ bị di chuyển (đổ) tối đa 1 lần trong suốt vòng đời của nó, nên độ phức tạp trung bình mỗi thao tác vẫn là O(1) dù trường hợp xấu nhất 1 lần gọi có thể là O(n)." — đây là phần **quan trọng nhất** cần nói rõ, vì nhiều người chỉ code đúng nhưng không giải thích được vì sao vẫn amortized O(1).
3. Nhắc use case thực tế: kỹ thuật 2-stack này còn dùng để cài đặt các cấu trúc khác (vd Min Stack, hoặc mô phỏng iterator).
4. Follow-up hay gặp (ngược lại): "Implement Stack using Queues" — bài đối xứng, dùng 1-2 queue để mô phỏng stack, cách làm là mỗi lần push, xoay vòng queue để phần tử mới luôn ở đầu — nên biết hướng nếu bị hỏi thêm.
5. Độ phức tạp: `push` O(1), `pop`/`peek` là O(1) amortized (worst case O(n) khi phải đổ), `empty` O(1).

---

# Bí quyết chung cho Linked List + Stack/Queue

**Linked List:**
- Luôn hỏi rõ edge case trước khi code: list rỗng? list chỉ có 1 node? có cần xử lý list có cycle không (với bài không liên quan cycle)?
- Kỹ thuật **Dummy Node** là "vũ khí" nên dùng bất cứ khi nào bài toán có khả năng thay đổi head (insert/delete/merge ở đầu list) — giúp code sạch hơn nhiều.
- Kỹ thuật **2 con trỏ nhanh/chậm (Fast & Slow Pointers)** không chỉ dùng cho detect cycle, còn dùng để tìm node giữa list, hay tìm node thứ k từ cuối — nên biết đây là 1 pattern lớn, không chỉ riêng bài cycle.
- Luôn vẽ hình khi giải thích — Linked List là dạng bài dễ nói nhầm bằng lời nhưng dễ hiểu khi vẽ.

**Stack/Queue:**
- Dấu hiệu dùng Stack: cần xử lý phần tử **gần nhất/mới nhất trước** (ngoặc, undo, duyệt biểu thức, DFS bằng iterative).
- Dấu hiệu dùng Queue: cần xử lý theo đúng **thứ tự đến trước** (BFS, xử lý tác vụ theo hàng đợi).
- Với bài "cài đặt cấu trúc A bằng cấu trúc B", luôn tìm insight: "thao tác nào của A cần được **đảo ngược 2 lần** để khớp với tính chất của B?" — đây chính là chìa khóa của bài Implement Queue using Stacks.
- Luôn phân tích rõ độ phức tạp **amortized** khi có thao tác "đôi khi mới cần làm" (như việc đổ stack) — thể hiện bạn hiểu sâu về phân tích độ phức tạp, không chỉ đếm vòng lặp đơn giản.

---

## Ghi chú về mức độ ưu tiên (theo bạn chia sẻ)
Với Zalo (và nhiều công ty tương tự ở mức medium), nhóm Tree/Graph/DP nặng ít xuất hiện hơn, nhưng **một vài bài cơ bản vẫn có thể bị hỏi** làm câu warm-up hoặc câu phụ. Nếu còn thời gian ôn, nên biết sơ qua (không cần đào sâu):
- **Tree cơ bản:** Maximum Depth of Binary Tree, Validate Binary Search Tree, Level Order Traversal (BFS) — đều dùng đệ quy hoặc queue đơn giản.
- **DP cơ bản:** Climbing Stairs, House Robber — đều là DP 1 chiều dễ, tương tự cách tư duy như Kadane's Algorithm đã ôn.

Nếu muốn, mình có thể làm thêm 1 file ngắn cho nhóm "phòng hờ" này để bạn yên tâm hơn trước buổi phỏng vấn.

Chúc bạn phỏng vấn thật tốt, tự tin lên nhé! 🍀
