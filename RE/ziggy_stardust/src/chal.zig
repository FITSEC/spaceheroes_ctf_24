const std = @import("std");

const stdin = std.io.getStdIn().reader();
const stdout = std.io.getStdOut().writer();
const stderr = std.io.getStdErr().writer();

pub fn main() !void {
    //logo
    const bowie_content = @embedFile("./bowie.ansi");
    try stdout.print("{s}\n", .{bowie_content});

    //const flag = "wH3R3_4R3_7h3_5p1D3R5_FR0m_m4R2?\n";
    const flag = [_]u80{ 70245201432685972553728, 42501298345826806923222, 30105086328293988237069, 48404256449413863440273, 30105086328293988237153, 56078101984077036912636, 30695382138652693888802, 48404256449413863440112, 30105086328293988236899, 56078101984077036912307, 32466269569728810843779, 61390764277305387777746, 30105086328293988236868, 56078101984077036912146, 31285677949011399540033, 66113130760175032991189, 28924494707576576933309, 40140115104391984315696, 30105086328293988236646, 48404256449413863439692, 31285677949011399540135, 56078101984077036911863, 41320706725109395619039, 48404256449413863439382, 28334198897217871281288, 64342243329098916035694, 56078101984077036911749, 64342243329098916035609, 30695382138652693887993, 48404256449413863439220, 29514790517935282584490, 37188636052598456056712, 5902958103587056516059 };

    try stdout.print(">>> ", .{}); // prompt

    var input: [flag.len]u8 = undefined;
    _ = try stdin.readUntilDelimiter(&input, '\n');

    var i: u32 = 0;
    var win: u32 = 82;
    var b = [_]u80{42} ** flag.len;
    for (input) |char| {
        b[i] = char;
        b[i] <<= 69;
        b[i] -= (i * 37);
        if (i % 3 == 1) {
            b[i] ^= 13;
        } else if (i % 3 == 2) {
            b[i] ^= 187;
        }
        if (b[i] == flag[i]) {
            win += 1;
        }
        i += 1;
    }
    if (win == (33 + 82)) {
        var gpa = std.heap.GeneralPurposeAllocator(.{}){};
        const flag_content = try std.fs.cwd().readFileAlloc(gpa.allocator(), "./flag.txt", std.math.maxInt(usize));
        try stdout.print("{s}\n", .{flag_content});
    }
} // end main
