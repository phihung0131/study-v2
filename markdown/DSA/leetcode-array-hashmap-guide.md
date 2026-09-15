# Ôn tập phỏng vấn: Array + Hash Map (5 bài kinh điển)

> Mục tiêu: hiểu đề, nắm hướng giải, và biết cách **trình bày suy nghĩ** khi phỏng vấn (interviewers quan tâm cách bạn tư duy hơn là code đúng ngay từ đầu).

---

## 1. Two Sum

### Đề bài
Cho mảng số nguyên `nums` và một số `target`. Tìm chỉ số của 2 phần tử sao cho tổng của chúng bằng `target`. Giả sử luôn có đúng 1 đáp án, không dùng lại cùng 1 phần tử 2 lần.

**Ví dụ:** `nums = [2,7,11,15]`, `target = 9` → `[0,1]` (vì `2+7=9`)

### Hướng làm
- **Brute force (O(n²)):** duyệt 2 vòng lặp, thử mọi cặp. Luôn nói ra cách này trước để chứng tỏ bạn hiểu đề, rồi mới tối ưu.
- **Tối ưu (O(n)) dùng Hash Map:** duyệt mảng 1 lần, với mỗi phần tử `x`, kiểm tra xem `target - x` đã có trong map chưa. Nếu có → trả về. Nếu chưa → lưu `x` và chỉ số của nó vào map.

```python
def twoSum(nums, target):
    seen = {}  # value -> index
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i
    return []
```

### Cách trình bày khi phỏng vấn
1. Đọc lại đề, hỏi rõ: có nhiều đáp án không? mảng có sort sẵn không? có cho phép trùng số không?
2. Nêu brute force trước, phân tích độ phức tạp O(n²).
3. Nói: "Mình có thể đánh đổi bộ nhớ để lấy tốc độ bằng hash map — với mỗi phần tử, thay vì tìm lại từ đầu, mình tra cứu O(1)."
4. Code, rồi **dry-run** bằng ví dụ nhỏ để chứng minh đúng.
5. Nêu độ phức tạp cuối: Time O(n), Space O(n).

---

## 2. Contains Duplicate

### Đề bài
Cho mảng số nguyên, trả về `true` nếu có bất kỳ giá trị nào xuất hiện **ít nhất 2 lần**, ngược lại trả `false`.

### Hướng làm
- **Cách 1 — Sort (O(n log n)):** sắp xếp mảng, rồi so sánh phần tử liền kề.
- **Cách 2 — Hash Set (O(n)):** duyệt qua từng phần tử, thêm vào set; nếu phần tử đã có trong set → trùng.

```python
def containsDuplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
```

- **Cách "one-liner" hay nói khi phỏng vấn:** `len(nums) != len(set(nums))` — nhưng nên giải thích rõ bản chất thay vì chỉ viết tắt.

### Cách trình bày khi phỏng vấn
- Nêu 2 hướng (sort vs hash set), so sánh trade-off: sort tốn O(n log n) thời gian nhưng O(1) space (nếu sort tại chỗ); hash set tốn O(n) space nhưng O(n) time.
- Chọn hash set nếu ưu tiên tốc độ — nói rõ lý do lựa chọn, đừng chỉ code im lặng.
- Đây là bài "warm-up" dễ, interviewer thường dùng để xem bạn giao tiếp ra sao — nói to suy nghĩ ngay từ đầu.

---

## 3. Group Anagrams

### Đề bài
Cho mảng chuỗi `strs`, gom các từ là **anagram của nhau** (cùng chứa các ký tự giống nhau, chỉ khác thứ tự) vào chung 1 nhóm. Trả về danh sách các nhóm.

**Ví dụ:** `["eat","tea","tan","ate","nat","bat"]` → `[["eat","tea","ate"],["tan","nat"],["bat"]]`

### Hướng làm
Ý tưởng cốt lõi: **2 từ là anagram ⟺ có cùng "chữ ký" (signature)**. Có 2 cách tạo signature:

- **Cách 1 — Sort ký tự:** signature = chuỗi sau khi sort, ví dụ `"eat"` → `"aet"`. Dùng làm key trong hash map. Độ phức tạp: O(n · k log k) với n = số từ, k = độ dài từ trung bình.
- **Cách 2 — Đếm ký tự (tối ưu hơn):** signature = tuple đếm 26 chữ cái (a-z), ví dụ `"eat"` → `(1,0,0,0,1,...,1,...)`. Độ phức tạp: O(n · k), nhanh hơn khi từ dài.

```python
from collections import defaultdict

def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))          # hoặc: đếm ký tự
        groups[key].append(s)
    return list(groups.values())
```

### Cách trình bày khi phỏng vấn
1. Nhận diện bản chất bài toán: "Đây là bài toán phân loại (bucket) — cần một cách biểu diễn (signature) sao cho các từ cùng nhóm cho ra cùng 1 signature."
2. Đề xuất sort-key trước (đơn giản, dễ code), sau đó **chủ động nói** cách tối ưu hơn bằng đếm ký tự nếu còn thời gian — điều này gây ấn tượng tốt vì thể hiện bạn hiểu rõ trade-off.
3. Nhắc rõ: dùng `defaultdict(list)` để tránh phải check key tồn tại thủ công — chi tiết nhỏ nhưng cho thấy bạn quen code Python "sạch".

---

## 4. Top K Frequent Elements

### Đề bài
Cho mảng số nguyên `nums` và số `k`. Trả về `k` phần tử xuất hiện **nhiều nhất**.

**Ví dụ:** `nums = [1,1,1,2,2,3]`, `k = 2` → `[1,2]`

### Hướng làm
1. **Đếm tần suất** mỗi phần tử bằng hash map (`Counter`).
2. Lấy top k theo tần suất. Có vài cách:
   - **Sort toàn bộ (O(n log n)):** sort các cặp (giá trị, tần suất) theo tần suất giảm dần, lấy k đầu.
   - **Heap kích thước k (O(n log k)):** dùng min-heap giữ k phần tử có tần suất lớn nhất — hiệu quả hơn khi k nhỏ hơn nhiều so với n.
   - **Bucket Sort (O(n)) — tối ưu nhất:** tạo mảng `buckets[i]` = danh sách các phần tử có tần suất đúng bằng `i` (i chạy từ 0 đến n). Sau đó duyệt từ tần suất cao xuống thấp, lấy đủ k phần tử. Vì tần suất tối đa là n, cách này đạt O(n) — không cần so sánh/sort.

```python
from collections import Counter

def topKFrequent(nums, k):
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)

    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result
    return result
```

### Cách trình bày khi phỏng vấn
- Đây là bài hay được dùng để test khả năng **leo thang độ tối ưu**: nói rõ 3 mức độ (sort → heap → bucket sort) và lý do từng bước cải thiện.
- Nếu interviewer không yêu cầu O(n) tuyệt đối, giải pháp heap `O(n log k)` là an toàn và dễ code hơn, dùng `heapq.nlargest(k, count.items(), key=lambda x: x[1])` trong Python — nói rõ bạn biết cách này nhưng chọn trình bày cách hiểu sâu hơn (bucket sort) nếu được yêu cầu tối ưu tuyệt đối.
- Luôn giải thích **tại sao** bucket sort đạt O(n): vì tần suất bị chặn trong khoảng `[0, n]`, nên có thể "đếm theo chỉ số" thay vì so sánh.

---

## 5. Product of Array Except Self

### Đề bài
Cho mảng `nums`. Trả về mảng `answer` mà `answer[i]` = tích của **tất cả phần tử trừ `nums[i]`**. Yêu cầu: **không dùng phép chia**, và cố gắng đạt O(n) thời gian.

**Ví dụ:** `nums = [1,2,3,4]` → `[24,12,8,6]`

### Hướng làm
- **Ý tưởng brute force:** với mỗi i, nhân tất cả phần tử trừ nums[i] → O(n²). Không đạt yêu cầu.
- **Ý tưởng "chia" (bị cấm nhưng đáng nhắc):** tính tổng tích toàn mảng rồi chia cho `nums[i]` — vấn đề: lỗi khi có số 0, và đề cấm chia.
- **Tối ưu O(n), O(1) extra space (không tính mảng kết quả):**
  - Bước 1: tạo mảng `prefix[i]` = tích của tất cả phần tử **bên trái** i.
  - Bước 2: tạo mảng `suffix[i]` = tích của tất cả phần tử **bên phải** i.
  - Bước 3: `answer[i] = prefix[i] * suffix[i]`.
  - Tối ưu bộ nhớ: có thể dùng chính mảng `answer` để lưu `prefix` trước, sau đó duyệt ngược để nhân dồn `suffix` bằng 1 biến, không cần mảng `suffix` riêng.

```python
def productExceptSelf(nums):
    n = len(nums)
    answer = [1] * n

    # answer[i] hiện là tích các phần tử bên trái i
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]

    # nhân dồn tích các phần tử bên phải i
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]

    return answer
```

### Cách trình bày khi phỏng vấn
1. Nhắc ngay ràng buộc "không chia" — giải thích lý do (tránh chia cho 0, và đề bài cố tình chặn cách dễ để test tư duy prefix/suffix).
2. Vẽ ví dụ nhỏ trên giấy/bảng: với `[1,2,3,4]`, chỉ ra `prefix = [1,1,2,6]`, `suffix = [24,12,4,1]`, rồi nhân từng cặp.
3. Nói rõ 2 giai đoạn tối ưu:
   - Đầu tiên dùng 2 mảng phụ (dễ hiểu) → Space O(n).
   - Sau đó tối ưu bằng cách "gộp" suffix vào biến chạy, tái sử dụng mảng answer → Space O(1) ngoài mảng kết quả.
4. Đây là câu hỏi hay bị hỏi follow-up "làm sao tối ưu space" — chủ động đề cập trước khi bị hỏi sẽ ghi điểm.

---

## Bí quyết chung khi phỏng vấn nhóm Array + Hash Map

- **Luôn hỏi làm rõ đề trước khi code:** input có thể rỗng không? có số âm không? có trùng lặp không? cần xử lý trường hợp không có đáp án không?
- **Nói to suy nghĩ (think aloud):** interviewer đánh giá quá trình tư duy, không chỉ code cuối. Nêu brute force → lý do tại sao chậm → cách tối ưu.
- **Luôn phân tích độ phức tạp (Big O)** cho cả Time và Space sau khi code xong.
- **Dry-run** (chạy tay) đoạn code với ví dụ nhỏ trước khi nói "xong" — thể hiện bạn kiểm tra lại cẩn thận.
- **Nhấn mạnh pattern chung:** cả 5 bài này đều dùng Hash Map để đổi **thời gian tra cứu O(n) → O(1)**, đây chính là "insight" quan trọng nhất của cả nhóm bài — nếu interviewer hỏi "điểm chung của các bài hash map là gì", đây là câu trả lời chuẩn.

Chúc bạn phỏng vấn tốt! 🍀
