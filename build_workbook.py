from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


def style_range(ws, cell_range, font=None, fill=None, border=None, alignment=None, num_format=None):
    for row in ws[cell_range]:
        for cell in row:
            if font:
                cell.font = font
            if fill:
                cell.fill = fill
            if border:
                cell.border = border
            if alignment:
                cell.alignment = alignment
            if num_format:
                cell.number_format = num_format


def auto_width(ws, min_width=12, max_width=44):
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            val = "" if cell.value is None else str(cell.value)
            if val.startswith("="):
                continue
            max_len = max(max_len, len(val))
        ws.column_dimensions[col_letter].width = max(min_width, min(max_width, max_len + 4))


def build_workbook(filename: str = "private_llm_model.xlsx") -> None:
    wb = Workbook()

    # Shared styles
    header_fill = PatternFill("solid", fgColor="1F4E78")
    sub_fill = PatternFill("solid", fgColor="D9E1F2")
    input_fill = PatternFill("solid", fgColor="FFF2CC")
    total_fill = PatternFill("solid", fgColor="E2EFDA")

    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    bold_font = Font(name="Calibri", size=11, bold=True, color="000000")
    input_font = Font(name="Calibri", size=11, color="0000FF")
    reg_font = Font(name="Calibri", size=11, color="000000")

    thin = Side(border_style="thin", color="BFBFBF")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    FMT_INR = "₹#,##0"
    FMT_INR_DEC = "₹#,##0.00"
    FMT_INT = "#,##0"
    FMT_DEC1 = "#,##0.0"
    FMT_DEC2 = "#,##0.00"
    FMT_PCT = "0.0%"

    # =========================================================================
    # SHEET 1: Inputs (Single Source of Truth)
    # =========================================================================
    ws_in = wb.active
    ws_in.title = "Inputs"
    ws_in.append(["Category", "Parameter", "Value", "Unit / Notes"])
    style_range(ws_in, "A1:D1", font=header_font, fill=header_fill, border=border)

    inputs_data = [
        # Hardware & VRAM (Rows 2-11)
        ("Hardware", "GPU VRAM (per card)", 48, "GB (RTX 6000 Ada)"),
        ("Hardware", "Alternative GPU VRAM", 96, "GB (sensitivity)"),
        ("Hardware", "Runtime VRAM Overhead", 0.10, "% of total VRAM"),
        ("Hardware", "Workstation CapEx (Sunk)", 1480000, "INR one-time"),
        ("Hardware", "Second GPU CapEx (Optional)", 890000, "INR one-time"),
        ("Hardware", "UPS & Cooling CapEx", 210000, "INR one-time"),
        ("Hardware", "UPS & Cooling Monthly OpEx", 6500, "INR/month"),
        ("Hardware", "Hardware Risk / Spares Reserve", 0.10, "% of HW CapEx over 3 yrs"),
        ("Power", "Load Power (1 GPU)", 1.20, "kW"),
        ("Power", "Idle Power (1 GPU)", 0.35, "kW"),
        # Rows 12-16
        ("Power", "2nd GPU Delta Load Power", 0.30, "kW"),
        ("Power", "2nd GPU Delta Idle Power", 0.05, "kW"),
        ("Power", "Electricity Tariff", 9.80, "INR/kWh"),
        ("People", "Lead AI Developer Annual CTC", 2400000, "INR/year"),
        ("People", "Junior Engineer Monthly Cost", 55000, "INR/month (from Apr 2027)"),
        # Rows 17-20
        ("People", "Junior Months in 3-Year Horizon", 32, "months (out of 36)"),
        ("Cloud", "Cloud Input Token Price", 42, "INR per 1M input tokens"),
        ("Cloud", "Cloud Output Token Price", 170, "INR per 1M output tokens"),
        ("Calendar", "Normal Days per Year", 243, "days"),
        ("Calendar", "Counselling Season Days per Year", 120, "days (Jun-Sep ex result)"),
        # Rows 21-29
        ("Calendar", "Result Days per Year", 2, "days (UG + PG)"),
        ("Traffic", "Normal Daily Chats", 1500, "chats/day"),
        ("Traffic", "Season Daily Chats", 22000, "chats/day"),
        ("Traffic", "Result Day Daily Chats", 60000, "chats/day"),
        ("Traffic", "Turns per Chat", 6, "turns/chat"),
        ("Traffic", "Peak Window Share (7-11 PM)", 0.70, "% of daily traffic"),
        ("Traffic", "Peak Window Duration", 4, "hours"),
        ("Traffic", "Queuing Allowance (Worst Hour)", 0.05, "% of chats queued"),
        ("Tokens", "Chat Prompt Tokens per Turn", 3200, "tokens"),
        # Rows 30-35
        ("Tokens", "Chat Output Tokens per Turn", 280, "tokens"),
        ("Cache", "Normal Day Cache Hit Rate", 0.30, "% served from cache"),
        ("Cache", "Counselling Season Cache Hit Rate", 0.50, "% served from cache"),
        ("Cache", "Result Day Cache Hit Rate", 0.70, "% served from cache"),
        ("Capacity", "Sustained Batched Decode (Model L)", 450, "output tok/s (1 GPU)"),
        ("Capacity", "Sustained Batched Decode (Model S+L)", 1000, "output tok/s blended (1 GPU)"),
        # Rows 36-46: Hirrx Match
        ("Hirrx", "Backlog Resumes", 240000, "resumes (Year 1)"),
        ("Hirrx", "Scanned Resume Share", 0.30, "% needing OCR"),
        ("Hirrx", "Open Jobs", 3500, "jobs"),
        ("Hirrx", "New Resumes per Week", 4000, "resumes/week"),
        ("Hirrx", "Resume Tokens (Parsed)", 1900, "tokens/resume"),
        ("Hirrx", "Job Description Tokens", 700, "tokens/JD"),
        ("Hirrx", "Cross-Encoder Top-K per Job", 50, "candidates/job"),
        ("Hirrx", "LLM Explanations Top-K per Job", 10, "candidates/job"),
        ("Hirrx", "LLM Explanation Prompt Overhead", 200, "tokens"),
        ("Hirrx", "LLM Explanation Output Tokens", 150, "tokens"),
        ("Hirrx", "Ongoing Weekly Re-rank Pairs", 40000, "pairs/week"),
        # Rows 47-51
        ("Hirrx", "Ongoing Weekly LLM Explanations", 5000, "explanations/week"),
        ("Hirrx", "Bi-Encoder Throughput (1 GPU)", 50000, "tokens/s"),
        ("Hirrx", "Cross-Encoder Throughput (1 GPU)", 30000, "tokens/s"),
        ("Hirrx", "LLM Batch Explain Speed (1 GPU)", 800, "output tok/s"),
        ("Rental", "Spare GPU Rental Rate", 175, "INR/GPU-hour"),
    ]

    pct_rows = {4, 9, 26, 28, 31, 32, 33, 37}
    inr_rows = {5, 6, 7, 8, 14, 15, 16, 17, 18, 51}
    dec2_rows = {10, 11, 12, 13, 14}

    for idx, row in enumerate(inputs_data, start=2):
        ws_in.append(list(row))
        style_range(ws_in, f"A{idx}:D{idx}", font=reg_font, border=border)
        c = ws_in[f"C{idx}"]
        c.font = input_font
        c.fill = input_fill
        if idx in pct_rows:
            c.number_format = FMT_PCT
        elif idx == 14:
            c.number_format = FMT_INR_DEC
        elif idx in inr_rows:
            c.number_format = FMT_INR
        elif idx in dec2_rows:
            c.number_format = FMT_DEC2
        else:
            c.number_format = FMT_INT

    # =========================================================================
    # SHEET 2: B1_KV_Cache
    # =========================================================================
    ws_kv = wb.create_sheet("B1_KV_Cache")
    ws_kv.append([
        "Model", "Layers (L)", "KV Heads", "Head Dim", "4-bit Weights (GB)",
        "Seq Len", "KV 16-bit (KiB/tok)", "KV 8-bit (KiB/tok)",
        "Free KV VRAM 48GB", "Concurrency 48GB (16-bit)", "Concurrency 48GB (8-bit)",
        "Free KV VRAM 96GB", "Concurrency 96GB (16-bit)", "Concurrency 96GB (8-bit)"
    ])
    style_range(ws_kv, "A1:N1", font=header_font, fill=header_fill, border=border)

    models = [
        ("Model S (8B)", 32, 8, 128, 5.2, 3500),
        ("Model M (14B)", 40, 8, 128, 8.9, 3500),
        ("Model L (32B)", 64, 8, 128, 19.0, 3500),
        ("Model XL (70B)", 80, 8, 128, 40.5, 3500),
    ]
    for r, (name, layers, nkv, dh, w4, seq) in enumerate(models, start=2):
        ws_kv.append([
            name, layers, nkv, dh, w4, seq,
            f"=(2*B{r}*C{r}*D{r}*2)/1024",
            f"=(2*B{r}*C{r}*D{r}*1)/1024",
            f"=Inputs!$C$2*(1-Inputs!$C$4)-E{r}",
            f"=INT(I{r}/((G{r}*F{r})/(1024*1024)))",
            f"=INT(I{r}/((H{r}*F{r})/(1024*1024)))",
            f"=Inputs!$C$3*(1-Inputs!$C$4)-E{r}",
            f"=INT(L{r}/((G{r}*F{r})/(1024*1024)))",
            f"=INT(L{r}/((H{r}*F{r})/(1024*1024)))",
        ])
        style_range(ws_kv, f"A{r}:N{r}", font=reg_font, border=border)
        for col in ["E", "I", "L"]:
            ws_kv[f"{col}{r}"].number_format = FMT_DEC1
        for col in ["G", "H", "J", "K", "M", "N"]:
            ws_kv[f"{col}{r}"].number_format = FMT_INT

    # =========================================================================
    # SHEET 3: B2_Traffic_Capacity
    # =========================================================================
    ws_tr = wb.create_sheet("B2_Traffic_Capacity")
    ws_tr.append([
        "Regime", "Days/Yr", "Chats/Day", "Raw Turns/Day", "Cache Hit Rate",
        "Uncached Turns/Day", "Peak Hr Raw Turns", "Peak Hr Uncached RPS",
        "Peak Prompt tok/s", "Peak Output tok/s", "Annual Uncached Turns",
        "Annual Input Tokens (M)", "Annual Output Tokens (M)", "Annual Load Hours (1 GPU)"
    ])
    style_range(ws_tr, "A1:N1", font=header_font, fill=header_fill, border=border)

    regimes = [
        ("Normal", "Inputs!$C$19", "Inputs!$C$22", "Inputs!$C$31"),
        ("Counselling Season", "Inputs!$C$20", "Inputs!$C$23", "Inputs!$C$32"),
        ("Result Day", "Inputs!$C$21", "Inputs!$C$24", "Inputs!$C$33"),
    ]
    for r, (name, days_ref, chats_ref, cache_ref) in enumerate(regimes, start=2):
        ws_tr.append([
            name,
            f"={days_ref}",
            f"={chats_ref}",
            f"=C{r}*Inputs!$C$25",
            f"={cache_ref}",
            f"=D{r}*(1-E{r})",
            f"=(D{r}*Inputs!$C$26)/Inputs!$C$27",
            f"=(G{r}*(1-E{r}))/3600",
            f"=H{r}*Inputs!$C$29",
            f"=H{r}*Inputs!$C$30",
            f"=B{r}*F{r}",
            f"=(K{r}*Inputs!$C$29)/1000000",
            f"=(K{r}*Inputs!$C$30)/1000000",
            f"=(M{r}*1000000)/(Inputs!$C$34*3600)",
        ])
        style_range(ws_tr, f"A{r}:N{r}", font=reg_font, border=border)
        ws_tr[f"E{r}"].number_format = FMT_PCT
        for col in ["B", "C", "D", "F", "G", "K"]:
            ws_tr[f"{col}{r}"].number_format = FMT_INT
        for col in ["H", "L", "M", "N"]:
            ws_tr[f"{col}{r}"].number_format = FMT_DEC2
        for col in ["I", "J"]:
            ws_tr[f"{col}{r}"].number_format = FMT_DEC1

    # Totals row (Row 5)
    ws_tr.append([
        "Annual Total", "=SUM(B2:B4)", "", "=SUMPRODUCT(B2:B4,D2:D4)", "",
        "", "", "", "", "", "=SUM(K2:K4)", "=SUM(L2:L4)", "=SUM(M2:M4)", "=SUM(N2:N4)"
    ])
    style_range(ws_tr, "A5:N5", font=bold_font, fill=total_fill, border=border)
    for col in ["B", "D", "K"]:
        ws_tr[f"{col}5"].number_format = FMT_INT
    for col in ["L", "M", "N"]:
        ws_tr[f"{col}5"].number_format = FMT_DEC2

    # Annual Chats helper (Row 7)
    ws_tr["A7"] = "Total Annual Chats"
    ws_tr["B7"] = "=SUMPRODUCT(B2:B4,C2:C4)"
    ws_tr["A7"].font = bold_font
    ws_tr["B7"].number_format = FMT_INT

    # =========================================================================
    # SHEET 4: B3_Hirrx_Night
    # =========================================================================
    ws_hx = wb.create_sheet("B3_Hirrx_Night")
    ws_hx.append(["Hirrx Workload Component", "Tokens (M)", "GPU-Hours", "Notes"])
    style_range(ws_hx, "A1:D1", font=header_font, fill=header_fill, border=border)

    hirrx_rows = [
        ("Backlog: Resume + JD Embeddings", "=(Inputs!$C$36*Inputs!$C$40+Inputs!$C$38*Inputs!$C$41)/1000000", "=(B2*1000000)/(Inputs!$C$48*3600)", "One-time Year 1"),
        ("Backlog: Cross-Encoder Re-rank", "=(Inputs!$C$38*Inputs!$C$42*(Inputs!$C$40+Inputs!$C$41))/1000000", "=(B3*1000000)/(Inputs!$C$49*3600)", "Top-50 per job"),
        ("Backlog: LLM Explanations (Input)", "=(Inputs!$C$38*Inputs!$C$43*(Inputs!$C$40+Inputs!$C$41+Inputs!$C$44))/1000000", 0, "Top-10 per job"),
        ("Backlog: LLM Explanations (Output)", "=(Inputs!$C$38*Inputs!$C$43*Inputs!$C$45)/1000000", "=(B5*1000000)/(Inputs!$C$50*3600)", "2-line explanation"),
        ("Total Backlog GPU-Hours", "", "=SUM(C2:C5)", "Fits in 2 overnight windows"),
        ("Ongoing Weekly: Embeddings", "=(Inputs!$C$39*Inputs!$C$40)/1000000", "=(B7*1000000)/(Inputs!$C$48*3600)", "4,000 resumes/wk"),
        ("Ongoing Weekly: Cross-Encoder", "=(Inputs!$C$46*(Inputs!$C$40+Inputs!$C$41))/1000000", "=(B8*1000000)/(Inputs!$C$49*3600)", "40,000 pairs/wk"),
        ("Ongoing Weekly: LLM Explain (In)", "=(Inputs!$C$47*(Inputs!$C$40+Inputs!$C$41+Inputs!$C$44))/1000000", 0, "5,000 explains/wk"),
        ("Ongoing Weekly: LLM Explain (Out)", "=(Inputs!$C$47*Inputs!$C$45)/1000000", "=(B10*1000000)/(Inputs!$C$50*3600)", "Output tokens"),
        ("Total Ongoing GPU-Hours / Week", "", "=SUM(C7:C10)", ""),
        ("Ongoing GPU-Hours / Night", "", "=C11/7", "7 nights/week"),
        ("Annual Hirrx GPU-Hours (Yr 1)", "", "=C6+C11*52", "Backlog + 52 wks"),
        ("Annual Hirrx GPU-Hours (Yr 2-3)", "", "=C11*52", "52 wks ongoing"),
    ]
    for r, row in enumerate(hirrx_rows, start=2):
        ws_hx.append(list(row))
        is_tot = r in {6, 11, 13, 14}
        style_range(ws_hx, f"A{r}:D{r}", font=bold_font if is_tot else reg_font, fill=total_fill if is_tot else None, border=border)
        ws_hx[f"B{r}"].number_format = FMT_DEC2
        ws_hx[f"C{r}"].number_format = FMT_DEC2

    # Spare Night Hours Block (Rows 16-22)
    ws_hx.append([])
    ws_hx.append(["Spare Night Capacity (11 PM - 7 AM = 8 hrs)", "Season Night", "Normal Night", "Annual Total"])
    style_range(ws_hx, "A16:D16", font=header_font, fill=header_fill, border=border)

    night_rows = [
        ("Night Chat Uncached Turns (8/20 of 30% off-peak)",
         "=B2_Traffic_Capacity!F3*(1-Inputs!$C$26)*(8/20)",
         "=B2_Traffic_Capacity!F2*(1-Inputs!$C$26)*(8/20)", ""),
        ("Night Chat GPU-Hours (@ Model L sustained)",
         "=(B17*Inputs!$C$30)/(Inputs!$C$34*3600)",
         "=(C17*Inputs!$C$30)/(Inputs!$C$34*3600)", ""),
        ("Ongoing Hirrx Night GPU-Hours", "=C12", "=C12", ""),
        ("Spare GPU-Hours / Night", "=8-B18-B19", "=8-C18-C19",
         "=B20*Inputs!$C$20+C20*Inputs!$C$19"),
        ("Potential Annual Rental Revenue (INR)", "", "", "=D20*Inputs!$C$51"),
    ]
    for r, row in enumerate(night_rows, start=17):
        ws_hx.append(list(row))
        is_tot = r in {20, 21}
        style_range(ws_hx, f"A{r}:D{r}", font=bold_font if is_tot else reg_font, fill=total_fill if is_tot else None, border=border)
        if r == 17:
            ws_hx[f"B{r}"].number_format = FMT_INT
            ws_hx[f"C{r}"].number_format = FMT_INT
        elif r == 21:
            ws_hx[f"D{r}"].number_format = FMT_INR
        else:
            for col in ["B", "C", "D"]:
                ws_hx[f"{col}{r}"].number_format = FMT_DEC2

    # =========================================================================
    # SHEET 5: F1_TCO_BreakEven
    # =========================================================================
    ws_tco = wb.create_sheet("F1_TCO_BreakEven")
    ws_tco.append(["3-Year TCO & Unit Economics (INR)", "On-Prem (1 GPU)", "On-Prem (2 GPUs)", "Hypothetical Cloud"])
    style_range(ws_tco, "A1:D1", font=header_font, fill=header_fill, border=border)

    # Helper formulas for 3-yr load hours and electricity
    # 3-yr load hrs = 3 * Chat_Load_Hrs + Hirrx_Yr1 + 2 * Hirrx_Yr2_3
    load_3yr = "(3*B2_Traffic_Capacity!N5+B3_Hirrx_Night!C13+2*B3_Hirrx_Night!C14)"
    elec_1gpu = f"=({load_3yr}*Inputs!$C$10+(3*8760-{load_3yr})*Inputs!$C$11)*Inputs!$C$13"
    elec_2gpu = f"=({load_3yr}*(Inputs!$C$10+Inputs!$C$12)+(3*8760-{load_3yr})*(Inputs!$C$11+Inputs!$C$12/6))*Inputs!$C$13"
    # Note: exact 2nd GPU idle delta is Inputs!$C$12? Wait: Row 12 is Delta Load, Row 13 is Delta Idle!
    # Let's double check exact row indices in Inputs!
    # Row 1: header
    # Row 2: GPU VRAM (48)
    # Row 3: Alt VRAM (96)
    # Row 4: Overhead (0.10)
    # Row 5: Workstation CapEx (1480000)
    # Row 6: 2nd GPU CapEx (890000)
    # Row 7: UPS CapEx (210000)
    # Row 8: UPS Monthly OpEx (6500)
    # Row 9: HW Risk Reserve (0.10)
    # Row 10: Load Power 1 GPU (1.20)
    # Row 11: Idle Power 1 GPU (0.35)
    # Row 12: 2nd GPU Delta Load Power (0.30)
    # Row 13: 2nd GPU Delta Idle Power (0.05)
    # Row 14: Electricity Tariff (9.80)
    # Row 15: Lead CTC (2400000)
    # Row 16: Junior Monthly (55000)
    # Row 17: Junior Months (32)
    # Row 18: Cloud Input Price (42)
    # Row 19: Cloud Output Price (170)
    # Row 20: Normal Days (243) -> WAIT! Let's fix the row indices above!

    # Let's verify exact row numbers of inputs_data cleanly using a lookup dict!
    ws_tco.delete_rows(1, ws_tco.max_row)
    wb.remove(ws_in)
    wb.remove(ws_kv)
    wb.remove(ws_tr)
    wb.remove(ws_hx)
    wb.remove(ws_tco)

    # Rebuild cleanly with programmatic row-reference dictionary so zero off-by-one errors can ever happen
    ws_in = wb.create_sheet("Inputs", 0)
    ws_in.append(["Category", "Parameter", "Value", "Unit / Notes"])
    style_range(ws_in, "A1:D1", font=header_font, fill=header_fill, border=border)

    ref = {}
    fmt_map = {}
    typed_inputs = [
        ("vram_48", "Hardware", "GPU VRAM (per card)", 48, "GB (RTX 6000 Ada)", FMT_INT),
        ("vram_96", "Hardware", "Alternative GPU VRAM", 96, "GB (sensitivity)", FMT_INT),
        ("vram_ovh", "Hardware", "Runtime VRAM Overhead", 0.10, "% of total VRAM", FMT_PCT),
        ("capex_ws", "Hardware", "Workstation CapEx (Sunk)", 1480000, "INR one-time", FMT_INR),
        ("capex_gpu2", "Hardware", "Second GPU CapEx (Optional)", 890000, "INR one-time", FMT_INR),
        ("capex_ups", "Hardware", "UPS & Cooling CapEx", 210000, "INR one-time", FMT_INR),
        ("opex_ups", "Hardware", "UPS & Cooling Monthly OpEx", 6500, "INR/month", FMT_INR),
        ("hw_risk", "Hardware", "Hardware Risk / Spares Reserve", 0.10, "% of HW CapEx (3 yrs)", FMT_PCT),
        ("pwr_load1", "Power", "Load Power (1 GPU)", 1.20, "kW", FMT_DEC2),
        ("pwr_idle1", "Power", "Idle Power (1 GPU)", 0.35, "kW", FMT_DEC2),
        ("pwr_dload2", "Power", "2nd GPU Delta Load Power", 0.30, "kW", FMT_DEC2),
        ("pwr_didle2", "Power", "2nd GPU Delta Idle Power", 0.05, "kW", FMT_DEC2),
        ("tariff", "Power", "Electricity Tariff", 9.80, "INR/kWh", FMT_INR_DEC),
        ("lead_ctc", "People", "Lead AI Developer Annual CTC", 2400000, "INR/year", FMT_INR),
        ("jr_mo", "People", "Junior Engineer Monthly Cost", 55000, "INR/month (from Apr 2027)", FMT_INR),
        ("jr_months", "People", "Junior Months in 3-Year Horizon", 32, "months (out of 36)", FMT_INT),
        ("cloud_in", "Cloud", "Cloud Input Token Price", 42, "INR per 1M input tokens", FMT_INR),
        ("cloud_out", "Cloud", "Cloud Output Token Price", 170, "INR per 1M output tokens", FMT_INR),
        ("days_norm", "Calendar", "Normal Days per Year", 243, "days", FMT_INT),
        ("days_seas", "Calendar", "Counselling Season Days per Year", 120, "days (Jun-Sep ex result)", FMT_INT),
        ("days_res", "Calendar", "Result Days per Year", 2, "days (UG + PG)", FMT_INT),
        ("chats_norm", "Traffic", "Normal Daily Chats", 1500, "chats/day", FMT_INT),
        ("chats_seas", "Traffic", "Season Daily Chats", 22000, "chats/day", FMT_INT),
        ("chats_res", "Traffic", "Result Day Daily Chats", 60000, "chats/day", FMT_INT),
        ("turns_chat", "Traffic", "Turns per Chat", 6, "turns/chat", FMT_INT),
        ("peak_share", "Traffic", "Peak Window Share (7-11 PM)", 0.70, "% of daily traffic", FMT_PCT),
        ("peak_hrs", "Traffic", "Peak Window Duration", 4, "hours", FMT_INT),
        ("queue_allow", "Traffic", "Queuing Allowance (Worst Hour)", 0.05, "% of chats queued", FMT_PCT),
        ("tok_prompt", "Tokens", "Chat Prompt Tokens per Turn", 3200, "tokens", FMT_INT),
        ("tok_out", "Tokens", "Chat Output Tokens per Turn", 280, "tokens", FMT_INT),
        ("cache_norm", "Cache", "Normal Day Cache Hit Rate", 0.30, "% served from cache", FMT_PCT),
        ("cache_seas", "Cache", "Counselling Season Cache Hit Rate", 0.50, "% served from cache", FMT_PCT),
        ("cache_res", "Cache", "Result Day Cache Hit Rate", 0.70, "% served from cache", FMT_PCT),
        ("tps_l", "Capacity", "Sustained Batched Decode (Model L)", 450, "output tok/s (1 GPU)", FMT_INT),
        ("tps_sl", "Capacity", "Sustained Batched Decode (Model S+L)", 1000, "output tok/s blended (1 GPU)", FMT_INT),
        ("hx_backlog", "Hirrx", "Backlog Resumes", 240000, "resumes (Year 1)", FMT_INT),
        ("hx_scan", "Hirrx", "Scanned Resume Share", 0.30, "% needing OCR", FMT_PCT),
        ("hx_jobs", "Hirrx", "Open Jobs", 3500, "jobs", FMT_INT),
        ("hx_wk_res", "Hirrx", "New Resumes per Week", 4000, "resumes/week", FMT_INT),
        ("hx_res_tok", "Hirrx", "Resume Tokens (Parsed)", 1900, "tokens/resume", FMT_INT),
        ("hx_jd_tok", "Hirrx", "Job Description Tokens", 700, "tokens/JD", FMT_INT),
        ("hx_ce_k", "Hirrx", "Cross-Encoder Top-K per Job", 50, "candidates/job", FMT_INT),
        ("hx_llm_k", "Hirrx", "LLM Explanations Top-K per Job", 10, "candidates/job", FMT_INT),
        ("hx_llm_ovh", "Hirrx", "LLM Explanation Prompt Overhead", 200, "tokens", FMT_INT),
        ("hx_llm_out", "Hirrx", "LLM Explanation Output Tokens", 150, "tokens", FMT_INT),
        ("hx_wk_ce", "Hirrx", "Ongoing Weekly Re-rank Pairs", 40000, "pairs/week", FMT_INT),
        ("hx_wk_llm", "Hirrx", "Ongoing Weekly LLM Explanations", 5000, "explanations/week", FMT_INT),
        ("hx_emb_tps", "Hirrx", "Bi-Encoder Throughput (1 GPU)", 50000, "tokens/s", FMT_INT),
        ("hx_ce_tps", "Hirrx", "Cross-Encoder Throughput (1 GPU)", 30000, "tokens/s", FMT_INT),
        ("hx_llm_tps", "Hirrx", "LLM Batch Explain Speed (1 GPU)", 800, "output tok/s", FMT_INT),
        ("rent_rate", "Rental", "Spare GPU Rental Rate", 175, "INR/GPU-hour", FMT_INR),
    ]

    for idx, (key, cat, param, val, unit, num_fmt) in enumerate(typed_inputs, start=2):
        ws_in.append([cat, param, val, unit])
        style_range(ws_in, f"A{idx}:D{idx}", font=reg_font, border=border)
        c = ws_in[f"C{idx}"]
        c.font = input_font
        c.fill = input_fill
        c.number_format = num_fmt
        ref[key] = f"Inputs!$C${idx}"

    # --- Sheet 2: B1_KV_Cache ---
    ws_kv = wb.create_sheet("B1_KV_Cache")
    ws_kv.append([
        "Model", "Layers (L)", "KV Heads", "Head Dim", "4-bit Weights (GB)",
        "Seq Len", "KV 16-bit (KiB/tok)", "KV 8-bit (KiB/tok)",
        "Free KV VRAM 48GB", "Concurrency 48GB (16-bit)", "Concurrency 48GB (8-bit)",
        "Free KV VRAM 96GB", "Concurrency 96GB (16-bit)", "Concurrency 96GB (8-bit)"
    ])
    style_range(ws_kv, "A1:N1", font=header_font, fill=header_fill, border=border)
    for r, (name, layers, nkv, dh, w4, seq) in enumerate(models, start=2):
        ws_kv.append([
            name, layers, nkv, dh, w4, seq,
            f"=(2*B{r}*C{r}*D{r}*2)/1024",
            f"=(2*B{r}*C{r}*D{r}*1)/1024",
            f"={ref['vram_48']}*(1-{ref['vram_ovh']})-E{r}",
            f"=INT(I{r}/((G{r}*F{r})/(1024*1024)))",
            f"=INT(I{r}/((H{r}*F{r})/(1024*1024)))",
            f"={ref['vram_96']}*(1-{ref['vram_ovh']})-E{r}",
            f"=INT(L{r}/((G{r}*F{r})/(1024*1024)))",
            f"=INT(L{r}/((H{r}*F{r})/(1024*1024)))",
        ])
        style_range(ws_kv, f"A{r}:N{r}", font=reg_font, border=border)
        for col in ["E", "I", "L"]:
            ws_kv[f"{col}{r}"].number_format = FMT_DEC1
        for col in ["G", "H", "J", "K", "M", "N"]:
            ws_kv[f"{col}{r}"].number_format = FMT_INT

    # --- Sheet 3: B2_Traffic_Capacity ---
    ws_tr = wb.create_sheet("B2_Traffic_Capacity")
    ws_tr.append([
        "Regime", "Days/Yr", "Chats/Day", "Raw Turns/Day", "Cache Hit Rate",
        "Uncached Turns/Day", "Peak Hr Raw Turns", "Peak Hr Uncached RPS",
        "Peak Prompt tok/s", "Peak Output tok/s", "Annual Uncached Turns",
        "Annual Input Tokens (M)", "Annual Output Tokens (M)", "Annual Load Hours (1 GPU)"
    ])
    style_range(ws_tr, "A1:N1", font=header_font, fill=header_fill, border=border)
    for r, (name, d_k, c_k, ch_k) in enumerate([
        ("Normal", "days_norm", "chats_norm", "cache_norm"),
        ("Counselling Season", "days_seas", "chats_seas", "cache_seas"),
        ("Result Day", "days_res", "chats_res", "cache_res"),
    ], start=2):
        ws_tr.append([
            name, f"={ref[d_k]}", f"={ref[c_k]}", f"=C{r}*{ref['turns_chat']}", f"={ref[ch_k]}",
            f"=D{r}*(1-E{r})", f"=(D{r}*{ref['peak_share']})/{ref['peak_hrs']}",
            f"=(G{r}*(1-E{r}))/3600", f"=H{r}*{ref['tok_prompt']}", f"=H{r}*{ref['tok_out']}",
            f"=B{r}*F{r}", f"=(K{r}*{ref['tok_prompt']})/1000000",
            f"=(K{r}*{ref['tok_out']})/1000000", f"=(M{r}*1000000)/({ref['tps_l']}*3600)"
        ])
        style_range(ws_tr, f"A{r}:N{r}", font=reg_font, border=border)
        ws_tr[f"E{r}"].number_format = FMT_PCT
        for col in ["B", "C", "D", "F", "G", "K"]:
            ws_tr[f"{col}{r}"].number_format = FMT_INT
        for col in ["H", "L", "M", "N"]:
            ws_tr[f"{col}{r}"].number_format = FMT_DEC2
        for col in ["I", "J"]:
            ws_tr[f"{col}{r}"].number_format = FMT_DEC1

    ws_tr.append([
        "Annual Total", "=SUM(B2:B4)", "", "=SUMPRODUCT(B2:B4,D2:D4)", "",
        "", "", "", "", "", "=SUM(K2:K4)", "=SUM(L2:L4)", "=SUM(M2:M4)", "=SUM(N2:N4)"
    ])
    style_range(ws_tr, "A5:N5", font=bold_font, fill=total_fill, border=border)
    for col in ["B", "D", "K"]:
        ws_tr[f"{col}5"].number_format = FMT_INT
    for col in ["L", "M", "N"]:
        ws_tr[f"{col}5"].number_format = FMT_DEC2

    ws_tr["A7"] = "Total Annual Chats"
    ws_tr["B7"] = "=SUMPRODUCT(B2:B4,C2:C4)"
    ws_tr["A7"].font = bold_font
    ws_tr["B7"].number_format = FMT_INT

    # --- Sheet 4: B3_Hirrx_Night ---
    ws_hx = wb.create_sheet("B3_Hirrx_Night")
    ws_hx.append(["Hirrx Workload Component", "Tokens (M)", "GPU-Hours", "Notes"])
    style_range(ws_hx, "A1:D1", font=header_font, fill=header_fill, border=border)
    hx_defs = [
        ("Backlog: Resume + JD Embeddings", f"=({ref['hx_backlog']}*{ref['hx_res_tok']}+{ref['hx_jobs']}*{ref['hx_jd_tok']})/1000000", f"=(B2*1000000)/({ref['hx_emb_tps']}*3600)", "One-time Year 1"),
        ("Backlog: Cross-Encoder Re-rank", f"=({ref['hx_jobs']}*{ref['hx_ce_k']}*({ref['hx_res_tok']}+{ref['hx_jd_tok']}))/1000000", f"=(B3*1000000)/({ref['hx_ce_tps']}*3600)", "Top-50 per job"),
        ("Backlog: LLM Explanations (Input)", f"=({ref['hx_jobs']}*{ref['hx_llm_k']}*({ref['hx_res_tok']}+{ref['hx_jd_tok']}+{ref['hx_llm_ovh']}))/1000000", 0, "Top-10 per job"),
        ("Backlog: LLM Explanations (Output)", f"=({ref['hx_jobs']}*{ref['hx_llm_k']}*{ref['hx_llm_out']})/1000000", f"=(B5*1000000)/({ref['hx_llm_tps']}*3600)", "2-line explanation"),
        ("Total Backlog GPU-Hours", "", "=SUM(C2:C5)", "Fits in 2 overnight windows"),
        ("Ongoing Weekly: Embeddings", f"=({ref['hx_wk_res']}*{ref['hx_res_tok']})/1000000", f"=(B7*1000000)/({ref['hx_emb_tps']}*3600)", "4,000 resumes/wk"),
        ("Ongoing Weekly: Cross-Encoder", f"=({ref['hx_wk_ce']}*({ref['hx_res_tok']}+{ref['hx_jd_tok']}))/1000000", f"=(B8*1000000)/({ref['hx_ce_tps']}*3600)", "40,000 pairs/wk"),
        ("Ongoing Weekly: LLM Explain (In)", f"=({ref['hx_wk_llm']}*({ref['hx_res_tok']}+{ref['hx_jd_tok']}+{ref['hx_llm_ovh']}))/1000000", 0, "5,000 explains/wk"),
        ("Ongoing Weekly: LLM Explain (Out)", f"=({ref['hx_wk_llm']}*{ref['hx_llm_out']})/1000000", f"=(B10*1000000)/({ref['hx_llm_tps']}*3600)", "Output tokens"),
        ("Total Ongoing GPU-Hours / Week", "", "=SUM(C7:C10)", ""),
        ("Ongoing GPU-Hours / Night", "", "=C11/7", "7 nights/week"),
        ("Annual Hirrx GPU-Hours (Yr 1)", "", "=C6+C11*52", "Backlog + 52 wks"),
        ("Annual Hirrx GPU-Hours (Yr 2-3)", "", "=C11*52", "52 wks ongoing"),
    ]
    for r, row in enumerate(hx_defs, start=2):
        ws_hx.append(list(row))
        is_tot = r in {6, 11, 13, 14}
        style_range(ws_hx, f"A{r}:D{r}", font=bold_font if is_tot else reg_font, fill=total_fill if is_tot else None, border=border)
        ws_hx[f"B{r}"].number_format = FMT_DEC2
        ws_hx[f"C{r}"].number_format = FMT_DEC2

    ws_hx.append([])
    ws_hx.append(["Spare Night Capacity (11 PM - 7 AM = 8 hrs)", "Season Night", "Normal Night", "Annual Total"])
    style_range(ws_hx, "A16:D16", font=header_font, fill=header_fill, border=border)
    night_defs = [
        ("Night Chat Uncached Turns (8/20 of 30% off-peak)",
         f"=B2_Traffic_Capacity!F3*(1-{ref['peak_share']})*(8/20)",
         f"=B2_Traffic_Capacity!F2*(1-{ref['peak_share']})*(8/20)", ""),
        ("Night Chat GPU-Hours (@ Model L sustained)",
         f"=(B17*{ref['tok_out']})/({ref['tps_l']}*3600)",
         f"=(C17*{ref['tok_out']})/({ref['tps_l']}*3600)", ""),
        ("Ongoing Hirrx Night GPU-Hours", "=C12", "=C12", ""),
        ("Spare GPU-Hours / Night", "=8-B18-B19", "=8-C18-C19",
         f"=B20*{ref['days_seas']}+C20*{ref['days_norm']}"),
        ("Potential Annual Rental Revenue (INR)", "", "", f"=D20*{ref['rent_rate']}"),
    ]
    for r, row in enumerate(night_defs, start=17):
        ws_hx.append(list(row))
        is_tot = r in {20, 21}
        style_range(ws_hx, f"A{r}:D{r}", font=bold_font if is_tot else reg_font, fill=total_fill if is_tot else None, border=border)
        if r == 17:
            ws_hx[f"B{r}"].number_format = FMT_INT
            ws_hx[f"C{r}"].number_format = FMT_INT
        elif r == 21:
            ws_hx[f"D{r}"].number_format = FMT_INR
        else:
            for col in ["B", "C", "D"]:
                ws_hx[f"{col}{r}"].number_format = FMT_DEC2

    # --- Sheet 5: F1_TCO_BreakEven ---
    ws_tco = wb.create_sheet("F1_TCO_BreakEven")
    ws_tco.append(["3-Year TCO & Unit Economics (INR)", "On-Prem (1 GPU)", "On-Prem (2 GPUs)", "Hypothetical Cloud"])
    style_range(ws_tco, "A1:D1", font=header_font, fill=header_fill, border=border)

    load_3yr = "(3*B2_Traffic_Capacity!N5+B3_Hirrx_Night!C13+2*B3_Hirrx_Night!C14)"
    cloud_chat_3yr = f"3*(B2_Traffic_Capacity!L5*{ref['cloud_in']}+B2_Traffic_Capacity!M5*{ref['cloud_out']})"
    cloud_hx_3yr = (
        f"((B3_Hirrx_Night!B4+3*52*B3_Hirrx_Night!B9)*{ref['cloud_in']}"
        f"+(B3_Hirrx_Night!B5+3*52*B3_Hirrx_Night!B10)*{ref['cloud_out']})"
    )

    tco_rows = [
        ("Workstation CapEx (Sunk)", f"={ref['capex_ws']}", f"={ref['capex_ws']}", 0),
        ("Second GPU CapEx", 0, f"={ref['capex_gpu2']}", 0),
        ("UPS & Cooling CapEx", f"={ref['capex_ups']}", f"={ref['capex_ups']}", 0),
        ("UPS & Cooling OpEx (36 months)", f"=36*{ref['opex_ups']}", f"=36*{ref['opex_ups']}", 0),
        ("Electricity (3 Years)",
         f"=({load_3yr}*{ref['pwr_load1']}+(3*8760-{load_3yr})*{ref['pwr_idle1']})*{ref['tariff']}",
         f"=({load_3yr}*({ref['pwr_load1']}+{ref['pwr_dload2']})+(3*8760-{load_3yr})*({ref['pwr_idle1']}+{ref['pwr_didle2']}))*{ref['tariff']}",
         0),
        ("Hardware Risk / Spares Reserve", f"=(B2+B3)*{ref['hw_risk']}", f"=(C2+C3)*{ref['hw_risk']}", 0),
        ("Cloud API: Chat (3 Years)", 0, 0, f"={cloud_chat_3yr}"),
        ("Cloud API: Hirrx LLM (3 Years)", 0, 0, f"={cloud_hx_3yr}"),
        ("Engineering Team (Lead 36m + Jr 32m)",
         f"=3*{ref['lead_ctc']}+{ref['jr_months']}*{ref['jr_mo']}",
         f"=3*{ref['lead_ctc']}+{ref['jr_months']}*{ref['jr_mo']}",
         f"=3*{ref['lead_ctc']}+{ref['jr_months']}*{ref['jr_mo']}"),
        ("Total 3-Year TCO (incl. Sunk)", "=SUM(B2:B10)", "=SUM(C2:C10)", "=SUM(D2:D10)"),
        ("Incremental 3-Year TCO (excl. Sunk)", "=B11-B2", "=C11-C2", "=D11"),
        ("3-Year Savings vs. Cloud (incl. Sunk)", "=D11-B11", "=D11-C11", 0),
        ("Cost per 1,000 Chats (All-in)", "=B11/(3*B2_Traffic_Capacity!B7/1000)", "=C11/(3*B2_Traffic_Capacity!B7/1000)", "=D11/(3*B2_Traffic_Capacity!B7/1000)"),
        ("Cost per 1,000 Chats (Infra / API Only)", "=(B11-B10)/(3*B2_Traffic_Capacity!B7/1000)", "=(C11-C10)/(3*B2_Traffic_Capacity!B7/1000)", "=(D11-D10)/(3*B2_Traffic_Capacity!B7/1000)"),
        ("Break-Even Chats vs. Cloud (incl. Sunk)", "=(B11-B10)/(D8/(3*B2_Traffic_Capacity!B7))", "=(C11-C10)/(D8/(3*B2_Traffic_Capacity!B7))", ""),
        ("Break-Even Years vs. Cloud (incl. Sunk)", "=B16/B2_Traffic_Capacity!B7", "=C16/B2_Traffic_Capacity!B7", ""),
    ]

    for r, row in enumerate(tco_rows, start=2):
        ws_tco.append(list(row))
        is_tot = r in {11, 12, 13}
        style_range(ws_tco, f"A{r}:D{r}", font=bold_font if is_tot else reg_font, fill=total_fill if is_tot else None, border=border)
        for col in ["B", "C", "D"]:
            if r == 16:
                ws_tco[f"{col}{r}"].number_format = FMT_INT
            elif r == 17:
                ws_tco[f"{col}{r}"].number_format = FMT_DEC2
            else:
                ws_tco[f"{col}{r}"].number_format = FMT_INR

    for ws in wb.worksheets:
        auto_width(ws)
        ws.freeze_panes = "A2"

    wb.save(filename)
    print(f"Saved {filename} successfully.")
