from manim import *

# def main():
#     print("Hello from manim-tut!")
#
#
# if __name__ == "__main__":
#     main()

class First(Scene):
    def construct(self):
        Text.set_default(font="Iosevka Nerd Font Mono")
        self.colors = [BLUE, GOLD, TEAL, RED, YELLOW, MAROON, GREEN, PURPLE]
        self.cptr = 0

        def get_color():
            c = self.colors[self.cptr]
            self.cptr += 1
            if self.cptr >= len(self.colors):
                self.cptr = 0
            return c

        superblock = Rectangle(width=4.0, height=1.0, color=BLUE)
        free_block_bitmap = Rectangle(width=4.0, height=1.0, color=RED)
        inodes = Rectangle(width=4.0, height=1.0, color=GREEN)
        files_and_dirs = Rectangle(width=4.0, height=4.0, color=PURPLE)

        rects = (
            VGroup(superblock, free_block_bitmap, inodes, files_and_dirs)
            .arrange(DOWN, buff=0.1)
            .shift(RIGHT * 1.5)
        )

        superblock_label = Text("Superblock", color=BLUE).scale(0.5)
        superblock_label.next_to(superblock, LEFT, buff=2)
        superblock_arrow = Arrow(
            start=superblock_label.get_right(),
            end=superblock.get_left(),
            buff=0.5,
            color=BLUE,
        )

        free_block_bitmap_label = Text(
            "Free Blocks Bitmap", color=RED).scale(0.5)
        free_block_bitmap_label.next_to(free_block_bitmap, LEFT, buff=2)
        free_block_bitmap_arrow = Arrow(
            start=free_block_bitmap_label.get_right(),
            end=free_block_bitmap.get_left(),
            buff=0.5,
            color=RED,
        )

        inodes_label = Text("Inodes", color=GREEN).scale(0.5)
        inodes_label.next_to(inodes, LEFT, buff=2)
        inodes_arrow = Arrow(
            start=inodes_label.get_right(), end=inodes.get_left(), buff=0.5, color=GREEN
        )

        files_and_dirs_label = Text(
            "Files and Directories", color=PURPLE).scale(0.5)
        files_and_dirs_label.next_to(files_and_dirs, LEFT, buff=2)
        files_and_dirs_arrow = Arrow(
            start=files_and_dirs_label.get_right(),
            end=files_and_dirs.get_left(),
            buff=0.5,
            color=PURPLE,
        )

        self.play(Create(rects))
        self.play(
            Create(superblock_label),
            Create(superblock_arrow),
            Create(inodes_label),
            Create(inodes_arrow),
            Create(free_block_bitmap_label),
            Create(free_block_bitmap_arrow),
            Create(files_and_dirs_label),
            Create(files_and_dirs_arrow),
        )
        self.wait(2)

        superblock = rects[0]
        rects.remove(superblock)
        self.add(superblock)
        self.play(*[FadeOut(o) for o in self.mobjects if o is not superblock])
        self.wait(1)

        magic_number = Rectangle(width=4.0, height=0.5)
        n_inode = Rectangle(width=4.0, height=0.5)
        n_inode_bitmap_blocks = Rectangle(width=4.0, height=0.5)
        n_blocks = Rectangle(width=4.0, height=1)
        max_file_size = Rectangle(width=4.0, height=0.5)
        block_size = Rectangle(width=4.0, height=0.5)
        root_inode_idx = Rectangle(width=4.0, height=0.5)
        next_free_inode_idx = Rectangle(width=4.0, height=0.5)
        padding = Rectangle(width=4.0, height=2.5)

        # self.play(superblock.animate.move_to(ORIGIN))
        rects = (
            VGroup(
                magic_number,
                n_inode,
                n_inode_bitmap_blocks,
                n_blocks,
                max_file_size,
                block_size,
                root_inode_idx,
                next_free_inode_idx,
                padding,
            )
            .arrange(DOWN, buff=0.1)
            .shift(RIGHT * 1.5)
        )
        fields = [
            "Magic Number",
            "Number of I-Nodes",
            "Number of Bitmap Blocks",
            "Number of Blocks",
            "Max File Size",
            "Block Size",
            "Root I-Node Position",
            "Next Free I-Node Index",
            "Padding",
        ]

        inner_text = [
            "u32: 0xDEADBEEF",
            "u16: ???",
            "u16: 1",
            "u16: DiskSize/BlockSize",
            "u16: 7KB",
            "u16: 1024B",
            "u16: 1",
            "u16: 1",
            "[0u8: 1024-Size so far]",
        ]
        arrows_and_labels = []
        for i in range(len(rects)):
            c = get_color()
            rects[i].set_stroke(c)

            label = Text(fields[i], color=c).shift(LEFT * 3).scale(0.5)
            label.next_to(rects[i], LEFT, buff=1)

            arrow = Arrow(start=label.get_right(),
                          end=rects[i].get_left(), color=c)
            arrow.next_to(label, RIGHT, buff=0.2)

            inner = (
                Text(inner_text[i], color=c).move_to(
                    rects[i].get_center()).scale(0.4)
            )

            arrows_and_labels.append(inner)
            arrows_and_labels.append(label)
            arrows_and_labels.append(arrow)
        self.play(Transform(superblock, rects))
        self.play(*[Create(o) for o in arrows_and_labels])
        self.wait(4)

        superblock = rects[0]
        rects.remove(superblock)
        self.add(superblock)
        self.play(*[FadeOut(o) for o in self.mobjects if o is not superblock])
        self.wait(1)


class LocateBlockInMap(Scene):
    def construct(self):
        Text.set_default(font="Iosevka Nerd Font Mono")
        bytes = []
        group = VGroup()
        for i in range(8):
            r = Rectangle(width=2, height=0.5).scale(0.75)
            group.add(r)
        group.arrange(RIGHT)
        for i in range(8):
            bits = Text("0000 0000").scale(0.5 * 0.75)
            bits.move_to(group[i].get_center())

            range_start = 8 * i
            range_end = (8 * (i + 1)) - 1
            r = Text(f"[{range_start} - {range_end}]").scale(0.35)
            r.move_to(group[i].get_bottom()).shift(DOWN * 0.5)

            bytes.append(bits)
            bytes.append(r)
        self.play(Create(group))
        self.play(*[Create(o) for o in bytes])
        self.wait(2)

        values = ["38", "38/8", "4.75", "int(4.75)", "4"]
        t = Text(values[0]).shift(UP * 2).scale(0.75)
        for v in values:
            newt = Text(v).shift(UP * 2).scale(0.75)
            self.play(TransformMatchingShapes(t, newt))
            t = newt
            self.wait(0.4)

        arrow = Arrow(start=t, end=group[4].get_center())
        self.play(Create(arrow))
        # byte = Text("8")
        # block_partition = Text("38/8")
        # self.play(Create(block_idx), Create(byte), Create(block_partition))

        byte = group[4]
        group.remove(byte)
        self.add(byte)
        self.play(*[FadeOut(o) for o in self.mobjects if o is not byte])
        self.play(byte.animate.move_to(ORIGIN))

        del group

        group = VGroup()
        for i in range(8):
            r = Rectangle(width=0.5, height=0.5).scale(0.75)
            group.add(r)
        group.arrange(RIGHT)
        bits = []
        for i in range(8):
            bit = Text("0").scale(0.5 * 0.75)
            bit.move_to(group[i].get_center())
            bits.append(bit)

            r = Text(f"{i}").scale(0.35)
            r.move_to(group[i].get_bottom()).shift(DOWN * 0.5)
            bits.append(r)

        self.play(Transform(byte, group))
        self.play(*[Create(o) for o in bits])

        values = ["38", "38%8", "6"]
        t = Text(values[0]).shift(UP * 2).scale(0.75)
        for v in values:
            newt = Text(v).shift(UP * 2).scale(0.75)
            self.play(TransformMatchingShapes(t, newt))
            t = newt
            self.wait(0.4)

        arrow = Arrow(start=t, end=group[6].get_center())
        self.play(Create(arrow))

        newt = Text("1", color=BLUE).move_to(group[6].get_center()).scale(0.5 * 0.75)
        self.play(Transform(bits[6*2], newt))

        self.wait(2)


