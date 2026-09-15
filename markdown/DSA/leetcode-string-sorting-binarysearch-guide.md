# Ôn tập phỏng vấn: String cơ bản + Sorting/Binary Search cơ bản

---

# PHẦN 1: STRING CƠ BẢN

## 1. Valid Anagram

### Đề bài
Cho 2 chuỗi `s` và `t`, kiểm tra `t` có phải là **anagram** của `s` không (cùng chứa các ký tự giống nhau với số lượng giống nhau, chỉ khác thứ tự).

**Ví dụ:** `s = "anagram"`, `t = "nagaram"` → `true`; `s = "rat"`, `t = "car"` → `false`

### Hướng làm
- **Điều kiện cần đầu tiên:** nếu `len(s) != len(t)` → chắc chắn `false`, trả về ngay (tối ưu sớm).
- **Cách 1 — Sort (O(n log n)):** sort cả 2 chuỗi, so sánh bằng nhau không.
- **Cách 2 — Đếm ký tự bằng Hash Map (O(n)):** đếm tần suất ký tự của `s`, rồi trừ dần theo `t`. Nếu có ký tự âm hoặc dư ở cuối → không phải anagram.

```python
from collections import Counter

def isAnagram(s, t):
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)
```

Hoặc viết tay không dùng `Counter` (để thể hiện hiểu bản chất):

```python
def isAnagram(s, t):
    if len(s) != len(t):
        return False
    count = [0] * 26
    for i in range(len(s)):
        count[ord(s[i]) - ord('a')] += 1
        count[ord(t[i]) - ord('a')] -= 1
    return all(c == 0 for c in count)
```

### Cách trình bày khi phỏng vấn
1. Đây là bài "khởi động" dễ — nói nhanh gọn 2 hướng, chọn hash map vì O(n) tốt hơn sort O(n log n).
2. Nhắc điều kiện biên: chuỗi rỗng, chuỗi khác độ dài, ký tự có phân biệt hoa/thường hay Unicode không — hỏi rõ trước khi code.
3. Nếu interviewer hỏi "tối ưu space", nói: dùng mảng cố định kích thước 26 (nếu chỉ có chữ thường a-z) thay vì hash map tổng quát → Space O(1) thay vì O(k) với k là số ký tự riêng biệt.
4. Follow-up hay gặp: "Nếu input là Unicode thì sao?" → mảng 26 không đủ, phải quay lại dùng hash map tổng quát.

---

## 2. Valid Parentheses (dùng Stack)

### Đề bài
Cho chuỗi `s` chỉ chứa các ký tự `'('`, `')'`, `'{'`, `'}'`, `'['`, `']'`. Kiểm tra chuỗi ngoặc có **hợp lệ** không (mỗi ngoặc mở phải có ngoặc đóng tương ứng, đúng thứ tự lồng nhau).

**Ví dụ:** `s = "()[]{}"` → `true`; `s = "(]"` → `false`; `s = "([)]"` → `false`

### Hướng làm
Đây là bài kinh điển thể hiện bản chất của **Stack** (ngăn xếp — vào sau ra trước, LIFO).

- **Ý tưởng:** duyệt qua từng ký tự:
  - Nếu là ngoặc **mở** (`(`, `{`, `[`) → đẩy vào stack.
  - Nếu là ngoặc **đóng** → kiểm tra đỉnh stack có phải ngoặc mở tương ứng không:
    - Nếu stack rỗng, hoặc đỉnh stack không khớp → `false` ngay.
    - Nếu khớp → pop khỏi stack.
  - Sau khi duyệt hết, nếu stack **rỗng** → hợp lệ; còn dư phần tử → không hợp lệ (ngoặc mở chưa được đóng).

```python
def isValid(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}

    for ch in s:
        if ch in pairs:  # ngoặc đóng
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
        else:  # ngoặc mở
            stack.append(ch)

    return not stack
```

### Cách trình bày khi phỏng vấn
1. Giải thích **tại sao Stack là cấu trúc phù hợp**: "Ngoặc đóng gần nhất phải khớp với ngoặc mở **gần nhất chưa đóng** — đây chính xác là tính chất LIFO của stack."
2. Nêu rõ 3 trường hợp khiến chuỗi **không hợp lệ** (nói to để interviewer thấy bạn nghĩ đầy đủ case):
   - Gặp ngoặc đóng nhưng stack rỗng (đóng thừa, không có gì để khớp).
   - Gặp ngoặc đóng nhưng không khớp với đỉnh stack (sai loại hoặc sai thứ tự lồng).
   - Duyệt hết chuỗi mà stack vẫn còn phần tử (ngoặc mở chưa đóng).
3. Dry-run ví dụ `"([)]"` để chỉ ra tại sao nó `false` dù số lượng từng loại ngoặc cân bằng — đây là bẫy hay gặp, chứng tỏ bạn hiểu rõ vấn đề không chỉ là đếm số ngoặc.
4. Độ phức tạp: Time O(n), Space O(n) (trường hợp xấu nhất toàn ngoặc mở).

---

## 3. Longest Palindromic Substring

### Đề bài
Cho chuỗi `s`, tìm **chuỗi con liên tiếp dài nhất** là palindrome (đọc xuôi ngược giống nhau).

**Ví dụ:** `s = "babad"` → `"bab"` hoặc `"aba"` (cả 2 đều đúng)

### Hướng làm
- **Brute force (O(n³)):** thử mọi chuỗi con, kiểm tra palindrome → quá chậm.
- **Cách phổ biến khi phỏng vấn — Expand Around Center (O(n²)):**
  - Insight: mọi palindrome đều có 1 **tâm** (center). Có 2 loại tâm: tâm là 1 ký tự (palindrome độ dài lẻ, vd `"aba"`) hoặc tâm là khoảng giữa 2 ký tự (độ dài chẵn, vd `"abba"`).
  - Với mỗi vị trí i từ 0 đến n-1, thử "nở rộng" ra 2 bên từ tâm i (lẻ) và từ tâm (i, i+1) (chẵn), miễn còn đối xứng thì tiếp tục mở rộng.
  - Theo dõi palindrome dài nhất tìm được.

```python
def longestPalindrome(s):
    if not s:
        return ""

    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]  # trả về chuỗi palindrome tìm được

    result = ""
    for i in range(len(s)):
        odd = expand(i, i)        # tâm lẻ
        even = expand(i, i + 1)   # tâm chẵn
        if len(odd) > len(result):
            result = odd
        if len(even) > len(result):
            result = even

    return result
```

- **Cách nâng cao hơn (nếu bị hỏi tối ưu O(n)):** thuật toán **Manacher's Algorithm** — thường KHÔNG cần nhớ chi tiết cho phỏng vấn thường, chỉ cần biết tên và nói "có tồn tại giải pháp O(n) là Manacher's Algorithm, nhưng phức tạp hơn nhiều để cài đặt đúng trong lúc phỏng vấn."

### Phiên bản dễ hơn (nếu muốn ôn nhẹ trước): **Valid Palindrome**
Chỉ cần kiểm tra 1 chuỗi có phải palindrome không (bỏ qua ký tự không phải chữ/số, không phân biệt hoa thường) — dùng **2 pointer** từ 2 đầu chuỗi vào giữa, so sánh từng cặp ký tự. Đây là bài nền tảng trước khi làm Longest Palindromic Substring.

### Cách trình bày khi phỏng vấn
1. Nêu ngay 2 loại tâm (lẻ/chẵn) — đây là điểm hay bị bỏ sót, nhiều người chỉ xử lý tâm lẻ và fail test case như `"abba"`.
2. Giải thích rõ hàm `expand`: mở rộng ra 2 bên trong lúc còn đối xứng, dừng ngay khi lệch hoặc chạm biên mảng.
3. Nêu độ phức tạp: có n tâm, mỗi lần mở rộng tối đa O(n) → tổng O(n²) thời gian, O(1) space ngoài kết quả.
4. Nếu bị hỏi "làm nhanh hơn được không" → nhắc đến DP (bảng `dp[i][j]` = chuỗi con từ i đến j có phải palindrome, O(n²) time/space) hoặc Manacher's O(n) — nói tên và ý tưởng chính, không cần code chi tiết trừ khi được yêu cầu.

---

# PHẦN 2: SORTING + BINARY SEARCH CƠ BẢN

## 4. Merge Intervals

### Đề bài
Cho danh sách các khoảng `intervals`, mỗi khoảng là `[start, end]`. Gộp tất cả các khoảng **chồng lấn (overlapping)** thành các khoảng không chồng lấn, bao phủ toàn bộ các khoảng đầu vào.

**Ví dụ:** `intervals = [[1,3],[2,6],[8,10],[15,18]]` → `[[1,6],[8,10],[15,18]]`

### Hướng làm
1. **Sort các khoảng theo `start`** — bước bắt buộc để đảm bảo các khoảng chồng lấn nằm gần nhau.
2. Duyệt qua từng khoảng đã sort, so với khoảng **cuối cùng đã gộp** trong kết quả:
   - Nếu `start` hiện tại ≤ `end` của khoảng cuối trong kết quả → **chồng lấn**, cập nhật `end` = `max(end cũ, end hiện tại)`.
   - Nếu không → không chồng lấn, thêm khoảng hiện tại như 1 khoảng mới vào kết quả.

```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    result = [intervals[0]]

    for start, end in intervals[1:]:
        last_end = result[-1][1]
        if start <= last_end:
            result[-1][1] = max(last_end, end)
        else:
            result.append([start, end])

    return result
```

### Cách trình bày khi phỏng vấn
1. Nhấn mạnh **tại sao phải sort trước**: "Nếu không sort, 2 khoảng chồng lấn có thể nằm cách xa nhau trong mảng, phải so sánh mọi cặp → O(n²). Sort theo `start` giúp chỉ cần so sánh với khoảng liền trước, đưa về O(n log n)."
2. Nêu rõ điều kiện chồng lấn: `start hiện tại <= end của khoảng trước` — dễ nhầm dấu `<` và `<=` (ví dụ `[1,4]` và `[4,5]` có được coi là chồng lấn không? Thường có, vì chạm nhau tại điểm 4) — nên hỏi rõ interviewer về edge case này.
3. Độ phức tạp: Time O(n log n) (do sort), Space O(n) cho kết quả.
4. Follow-up hay gặp: "Insert Interval" (chèn 1 khoảng mới vào danh sách đã sort và merge) — bản chất tương tự nhưng không cần sort lại từ đầu.

---

## 5. Search in Rotated Sorted Array

### Đề bài
Cho mảng `nums` đã sort tăng dần nhưng bị **xoay (rotate)** tại 1 điểm không biết trước (vd `[0,1,2,4,5,6,7]` → `[4,5,6,7,0,1,2]`). Tìm chỉ số của `target` trong mảng, nếu không có trả về -1. Yêu cầu: O(log n).

**Ví dụ:** `nums = [4,5,6,7,0,1,2]`, `target = 0` → `4`

### Hướng làm
Đây là **Binary Search biến thể** — vẫn chia đôi mỗi bước, nhưng cần xác định thêm **nửa nào đang được sort** để quyết định thu hẹp phạm vi tìm kiếm về bên nào.

- Tại mỗi bước, tính `mid`. Nếu `nums[mid] == target` → xong.
- So sánh `nums[left]` với `nums[mid]` để biết **nửa trái `[left, mid]` có đang sort không**:
  - Nếu `nums[left] <= nums[mid]` → nửa trái đang sort bình thường.
    - Nếu `target` nằm trong khoảng `[nums[left], nums[mid])` → thu hẹp `right = mid - 1`.
    - Ngược lại → `left = mid + 1`.
  - Ngược lại → nửa **phải** `[mid, right]` đang sort.
    - Nếu `target` nằm trong khoảng `(nums[mid], nums[right]]` → thu hẹp `left = mid + 1`.
    - Ngược lại → `right = mid - 1`.

```python
def search(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid

        if nums[left] <= nums[mid]:  # nửa trái đang sort
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # nửa phải đang sort
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1
```

### Cách trình bày khi phỏng vấn
1. Nêu insight cốt lõi ngay từ đầu: "Dù mảng bị xoay, **luôn có ít nhất 1 nửa (trái hoặc phải quanh mid) vẫn đang sort bình thường**. Mình xác định nửa nào sort, rồi kiểm tra target có nằm trong khoảng của nửa sort đó không để quyết định thu hẹp." Đây là câu giải thích quan trọng nhất của cả bài.
2. Vẽ ví dụ trên giấy/bảng, chỉ rõ `left, mid, right` và nửa nào sort tại từng bước.
3. Cẩn thận điều kiện biên `<=` vs `<` khi kiểm tra target nằm trong khoảng — nói rõ bạn đang cân nhắc kỹ để tránh off-by-one.
4. Độ phức tạp: Time O(log n), Space O(1).
5. Follow-up hay gặp: "Nếu mảng có phần tử trùng lặp thì sao?" → trường hợp `nums[left] == nums[mid]` không thể xác định nửa nào sort, phải giảm `left += 1` để thu hẹp dần (worst case xuống O(n)) — nên biết để trả lời nếu bị hỏi thêm (đây là bài Search in Rotated Sorted Array II).

---

## 6. Find Minimum in Rotated Sorted Array

### Đề bài
Cho mảng `nums` đã sort tăng dần rồi bị xoay tại 1 điểm không biết trước, không có phần tử trùng lặp. Tìm phần tử **nhỏ nhất**. Yêu cầu O(log n).

**Ví dụ:** `nums = [3,4,5,1,2]` → `1`

### Hướng làm
Bài này là nền tảng, đơn giản hơn bài 5 — chỉ cần dùng Binary Search để tìm "điểm xoay" (pivot point), chính là phần tử nhỏ nhất.

- **Insight:** phần tử nhỏ nhất chính là điểm mà thứ tự tăng dần bị "gãy". So sánh `nums[mid]` với `nums[right]`:
  - Nếu `nums[mid] > nums[right]` → điểm nhỏ nhất nằm ở **nửa phải** (sau mid), vì nếu nửa `[mid, right]` mà `nums[mid] > nums[right]` thì chắc chắn có điểm gãy trong đó → `left = mid + 1`.
  - Nếu `nums[mid] <= nums[right]` → nửa `[mid, right]` đang sort bình thường, nghĩa là điểm nhỏ nhất nằm ở **nửa trái (bao gồm cả mid)** → `right = mid` (giữ lại mid, không loại nó vì có thể chính nó là min).
- Lặp đến khi `left == right` → đó chính là vị trí phần tử nhỏ nhất.

```python
def findMin(nums):
    left, right = 0, len(nums) - 1

    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    return nums[left]
```

### Cách trình bày khi phỏng vấn
1. So sánh với `nums[right]` (không phải `nums[left]`) — giải thích lý do: so với `right` giúp phân biệt rõ ràng nửa nào chứa điểm gãy mà không cần thêm điều kiện phụ.
2. Nhấn mạnh vì sao dùng `right = mid` (giữ nguyên mid) thay vì `right = mid - 1`: vì `mid` **có thể chính là đáp án** (phần tử nhỏ nhất), không được loại bỏ nó ra khỏi phạm vi tìm kiếm.
3. Dry-run với `[3,4,5,1,2]` từng bước để chỉ ra `left, right` hội tụ về index 3 (giá trị 1) ra sao.
4. Đây là bài rất hay dùng làm "bước đệm" trước bài Search in Rotated Sorted Array — nếu bị hỏi liên tiếp cả 2 bài, nên nhắc: "Ý tưởng ở đây giống bài tìm kiếm target ở trên, chỉ khác là mình luôn so sánh để tìm điểm gãy thay vì tìm giá trị cụ thể."
5. Độ phức tạp: Time O(log n), Space O(1).

---

# Bí quyết chung cho 2 nhóm này

**String cơ bản:**
- Luôn hỏi rõ về bảng ký tự (chỉ chữ thường a-z, hay có Unicode/số/ký tự đặc biệt) — ảnh hưởng đến việc chọn mảng cố định (O(1) space) hay hash map tổng quát.
- Với bài liên quan Stack (ngoặc, biểu thức), luôn tự hỏi: "Phần tử nào cần xử lý trước — cái mới nhất hay cũ nhất?" Nếu là mới nhất → Stack (LIFO) là lựa chọn đúng.
- Với Palindrome, luôn nhớ **2 loại tâm** (lẻ/chẵn) khi dùng expand-around-center.

**Sorting + Binary Search:**
- Dấu hiệu cần **sort trước**: bài toán liên quan đến khoảng (interval), hoặc cần so sánh phần tử với "hàng xóm" mà thứ tự ban đầu không quan trọng.
- Dấu hiệu dùng **Binary Search biến thể**: đề bài nói "mảng đã sort" (dù có bị xoay/biến đổi) và yêu cầu O(log n) — đây là tín hiệu rất rõ ràng, cứ thấy "sorted array" + "O(log n)" là nghĩ ngay đến binary search.
- Với binary search biến thể (rotated array), luôn xác định **nửa nào đang sort bình thường** trước khi quyết định thu hẹp phạm vi — đây là kỹ thuật lặp lại ở nhiều bài dạng này.
- Luôn cẩn thận về **off-by-one** (`<` vs `<=`, `mid` vs `mid ± 1`) — nói to cách bạn suy luận điều kiện biên để interviewer thấy bạn kiểm soát chi tiết, không đoán mò.

Chúc bạn phỏng vấn thật tốt! 🍀
