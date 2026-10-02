using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using cvoluşturma.Data;
using cvoluşturma.Models;

var builder = WebApplication.CreateBuilder(args);

var connectionString = builder.Configuration.GetConnectionString("DefaultConnection") ?? "Data Source=app.db";
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite(connectionString));

builder.Services.AddIdentity<ApplicationUser, IdentityRole>(options => {
    options.Password.RequireDigit = false;
    options.Password.RequiredLength = 6;
    options.Password.RequireNonAlphanumeric = false;
    options.Password.RequireUppercase = false;
    options.Password.RequireLowercase = false;

    // Brute-Force Koruması: 5 başarısız denemede 15 dakika kilitle
    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(15);
    options.Lockout.MaxFailedAccessAttempts = 5;
    options.Lockout.AllowedForNewUsers = true;

    // E-posta benzersizliği zorunlu
    options.User.RequireUniqueEmail = true;
})
.AddEntityFrameworkStores<AppDbContext>()
.AddDefaultTokenProviders();


builder.Services.AddControllersWithViews();

var app = builder.Build();

// Ensure DB is created
using (var scope = app.Services.CreateScope())
{
    var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    context.Database.EnsureCreated();
}

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseRouting();

app.UseAuthentication();
app.UseAuthorization();

// =============================================
// Güvenlik HTTP Başlıkları (Security Headers)
// =============================================
app.Use(async (context, next) =>
{
    var headers = context.Response.Headers;

    // Clickjacking koruması: Sayfa baska sitelerde iframe olarak açilamaz
    headers["X-Frame-Options"] = "DENY";

    // MIME Sniffing koruması: Tarayıcı dosya türünü tahmin etmeye çalışmaz
    headers["X-Content-Type-Options"] = "nosniff";

    // Referrer bilgisi sadece aynı origin içinde paylaşılır
    headers["Referrer-Policy"] = "strict-origin-when-cross-origin";

    // CSP: Yalnızca güvenilir kaynaklardan script/style/font yüklenmesine izin ver
    headers["Content-Security-Policy"] =
        "default-src 'self'; " +
        "script-src 'self' 'unsafe-inline' " +
            "https://cdnjs.cloudflare.com " +
            "https://cdn.quilljs.com " +
            "https://cdn.jsdelivr.net " +
            "https://cdn.bootstrapcdn.com; " +
        "style-src 'self' 'unsafe-inline' " +
            "https://cdn.quilljs.com " +
            "https://cdn.bootstrapcdn.com " +
            "https://fonts.googleapis.com " +
            "https://cdnjs.cloudflare.com; " +
        "font-src 'self' " +
            "https://fonts.googleapis.com " +
            "https://fonts.gstatic.com " +
            "https://cdnjs.cloudflare.com; " +
        "img-src 'self' data: blob: https:; " +
        "connect-src 'self'; " +
        "object-src 'none'; " +
        "base-uri 'self'; " +
        "form-action 'self';";

    await next();
});

app.MapStaticAssets();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}")
    .WithStaticAssets();

app.Run();
