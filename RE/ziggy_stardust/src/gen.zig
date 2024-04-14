const std = @import("std");

pub fn main() !void {
    const flag = "wH3R3_4R3_7h3_5p1D3R5_FR0m_m4R2?\n";

    var input: [flag.len]u8 = undefined;

    const stdin = std.io.getStdIn().reader();
    const stdout = std.io.getStdOut().writer();

    _ = try stdin.readUntilDelimiter(&input, '\n');

    try stdout.print("The user entered: {s}\n", .{input});

    var b = [_]u80{42} ** flag.len;
    var i: u32 = 0;
    var win: u32 = 0;
    for (input) |char| {
        b[i] = char;
        b[i] <<= 69;
        b[i] -= (i * 37);
        if (i % 3 == 1) {
            b[i] ^= 13;
        } else if (i % 3 == 2) {
            b[i] ^= 187;
        }
        try stdout.print("{d}\n", .{b[i]});
        if (b[i] == flag[i]) {
            win += 1;
        }
        i += 1;
    }
    //try stdout.print("{d}\n", .{win});
}
